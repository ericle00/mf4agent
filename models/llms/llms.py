import functools

# ------------------------ Typing -------------------------- #
from typing import (
    Any,
    Dict,
    List,
    Awaitable,
    Callable,
    Optional,
    Sequence,
    Union,
    cast,
    get_args,
)

from llama_index.core.tools.types import BaseTool
from llama_index.core.tools import FunctionTool, QueryEngineTool


# ------------------------ Pydantic -------------------------- #
from llama_index.core.bridge.pydantic import Field


# ------------------------ Decorators -------------------------- #
from llama_index.core.base.llms.generic_utils import (
    achat_to_completion_decorator,
    acompletion_to_chat_decorator,
    astream_chat_to_completion_decorator,
    astream_completion_to_chat_decorator,
    chat_to_completion_decorator,
    completion_to_chat_decorator,
    stream_chat_to_completion_decorator,
    stream_completion_to_chat_decorator,
)

# ------------------------ LLMs -------------------------- #
from llama_index.core.llms import (
    LLMMetadata,
)

from llama_index.core.llms.function_calling import (
    FunctionCallingLLM
)

from llama_index.core.base.llms.types import (
    ChatMessage,
    ChatResponse,
    ChatResponseAsyncGen,
    ChatResponseGen,
    CompletionResponse,
    CompletionResponseAsyncGen,
    CompletionResponseGen,
    LLMMetadata,
    MessageRole,
)

from llama_index.core.llms.callbacks import (
    llm_chat_callback,
    llm_completion_callback,
)

from llama_index.core.llms.llm import ToolSelection

from llama_index.core.llms.utils import parse_partial_json


# ------------------------ Callbacks -------------------------- #
from llama_index.core.callbacks import CallbackManager

from llama_index.llms.openai.utils import (
    OpenAIToolCall,
    create_retry_decorator,
    from_openai_completion_logprobs,
    from_openai_message,
    from_openai_token_logprobs,
    is_chat_model,
    is_function_calling_model,
    openai_modelname_to_contextsize,
    resolve_openai_credentials,
    to_openai_message_dicts,
)

# ------------------------ Open AI -------------------------- #
from openai import AsyncOpenAI
from openai import OpenAI as SyncOpenAI

from openai.types.chat.chat_completion_chunk import (
    ChatCompletionChunk,
    ChoiceDelta,
    ChoiceDeltaToolCall,
)

from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall, 
    Function
)


# ------------------------ My help functions -------------------------- #
import uuid
import re, json

# ------------------------ Constants -------------------------- #
DEFAULT_OPEN_SOURCE_MODEL = "llama-31-70b"
DEFAULT_TEMPERATURE = 0.0


def llm_retry_decorator(f: Callable[[Any], Any]) -> Callable[[Any], Any]:
    @functools.wraps(f)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        max_retries = getattr(self, "max_retries", 0)
        if max_retries <= 0:
            return f(self, *args, **kwargs)

        retry = create_retry_decorator(
            max_retries=max_retries,
            random_exponential=True,
            stop_after_delay_seconds=60,
            min_seconds=1,
            max_seconds=20,
        )
        return retry(f)(self, *args, **kwargs)

    return wrapper


class OpenAICoreML(FunctionCallingLLM):
    """
    OpenAI LLM. Adapted from llama index OpenAI Integration

    Args:
        model: name of the open source llama model to use. Choose between LLama 31 70B or 405B
        temperature: a float from 0 to 1 controlling randomness in generation; higher will lead to more creative, less deterministic responses.
        max_tokens: the maximum number of tokens to generate.
        additional_kwargs: Add additional parameters to OpenAI request body.
        max_retries: How many times to retry the API call if it fails.
        timeout: How long to wait, in seconds, for an API call before failing.
        reuse_client: Reuse the OpenAI client between requests. When doing anything with large volumes of async API calls, setting this to false can improve stability.
        api_key: Your OpenAI api key
        api_base: The base URL of the API to call
        callback_manager: the callback manager is used for observability.
    """
    # Model settings
    model: str = Field(
        default=DEFAULT_OPEN_SOURCE_MODEL, description="The OpenAI model to use."
    )
    temperature: float = Field(
        default=DEFAULT_OPEN_SOURCE_MODEL,
        description="The temperature to use during generation.",
        gte=0.0,
        lte=1.0,
    )
    max_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate.",
        gt=0,
    )

    # Client settings
    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional kwargs for the OpenAI API."
    )
    max_retries: int = Field(
        default=3,
        description="The maximum number of API retries.",
        gte=0,
    )
    timeout: float = Field(
        default=60.0,
        description="The timeout, in seconds, for API requests.",
        gte=0,
    )
    reuse_client: bool = Field(
        default=True,
        description=(
            "Reuse the OpenAI client between requests. When doing anything with large "
            "volumes of async API calls, setting this to false can improve stability."
        ),
    )

    # API
    api_key: str = Field(default=None, description="The OpenAI Core ML API key.")
    api_base: str = Field(description="The base URL for Core ML OpenAI.")
    
    # LLM metadata
    context_window: int = 128000
    model_name: str = DEFAULT_OPEN_SOURCE_MODEL
    is_chat_model: bool = True
    is_function_calling_model: bool = True
    
    # ------------------------ Init -------------------------- #

    def __init__(
        self,
        model: str = DEFAULT_OPEN_SOURCE_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = 128000,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
        timeout: float = 60.0,
        reuse_client: bool = True,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ):
        additional_kwargs = additional_kwargs or {}

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            additional_kwargs=additional_kwargs,
            max_retries=max_retries,
            timeout=timeout,
            reuse_client=reuse_client,
            api_key=api_key,
            api_base=api_base,
            callback_manager=callback_manager,
            **kwargs,
        )
        self._client = None
        self._aclient = None
        
    # ------------------------ Get kwargs -------------------------- #

    def _get_credential_kwargs(self) -> Dict[str, Any]:
        """
        Returns a dictionary of credentials required to instantiate the OpenAI client.
        """
        return {
            "api_key": self.api_key,
            "base_url": self.api_base,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
        }
        
    def _get_model_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Returns a dictionary of model parameters with optional overrides from kwargs. 
        Ensures streaming options are excluded if not applicable.
        """
        base_kwargs = {
            "model": self.model, 
            "temperature": self.temperature, 
            **kwargs,
        }
        if self.max_tokens is not None:
            base_kwargs["max_tokens"] = self.max_tokens

        # can't send stream_options to the API when not streaming
        all_kwargs = {
            **base_kwargs, 
            **self.additional_kwargs,
        }
        
        if "stream" not in all_kwargs and "stream_options" in all_kwargs:
            del all_kwargs["stream_options"]

        return all_kwargs
    
    # ------------------------ Clients -------------------------- #

        
    def _get_client(self) -> SyncOpenAI:
        """
        Returns a synchronous OpenAI client.
        """
        # Create a new SyncOpenAI client if reuse_client is False
        if not self.reuse_client:
            return SyncOpenAI(**self._get_credential_kwargs())
        
        # Reuse the existing client if available, otherwise create a new one
        if self._client is None:
            self._client = SyncOpenAI(**self._get_credential_kwargs())
            
        return self._client


    def _get_aclient(self) -> AsyncOpenAI:
        """
        Returns an asynchronous OpenAI client.
        """
        # Create a new AsyncOpenAI client if reuse_client is False
        if not self.reuse_client:
            return AsyncOpenAI(**self._get_credential_kwargs())
        
        # Reuse the existing client if available, otherwise create a new one
        if self._aclient  is None:
            self._aclient  = AsyncOpenAI(**self._get_credential_kwargs())
            
        return self._aclient 
    
    
    # ------------------------ Meta data -------------------------- #
    @classmethod
    def class_name(cls) -> str:
        """Get the class name, used as a unique ID in serialization."""
        return "openai_coreml_llm"
    
    
    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.max_tokens or -1,
            is_chat_model=self.is_chat_model,
            is_function_calling_model=self.is_function_calling_model,
            model_name=self.model_name,
        )
    
    # ------------------------ Synced Endpoints -------------------------- #
    # ------------------------ Base Chat Functions -------------------------- #
    
    @llm_chat_callback()
    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        if self._use_chat_completions(kwargs):
            chat_fn = self._chat
        else:
            chat_fn = completion_to_chat_decorator(self._complete)
        return chat_fn(messages, **kwargs)
    
    
    @llm_chat_callback()
    def stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        if self._use_chat_completions(kwargs):
            stream_chat_fn = self._stream_chat
        else:
            stream_chat_fn = stream_completion_to_chat_decorator(self._stream_complete)
        return stream_chat_fn(messages, **kwargs)
    
    
    @llm_completion_callback()
    def complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if self._use_chat_completions(kwargs):
            complete_fn = chat_to_completion_decorator(self._chat)
        else:
            complete_fn = self._complete
        return complete_fn(prompt, **kwargs)


    @llm_completion_callback()
    def stream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        if self._use_chat_completions(kwargs):
            stream_complete_fn = stream_chat_to_completion_decorator(self._stream_chat)
        else:
            stream_complete_fn = self._stream_complete
        return stream_complete_fn(prompt, **kwargs)
    
    
    def _use_chat_completions(self, kwargs: Dict[str, Any]) -> bool:
        """
        Checks if chat completions should be used from metadata.
        """
        if "use_chat_completions" in kwargs:
            return kwargs["use_chat_completions"]
        return self.metadata.is_chat_model
    
    # ------------------------ Class Functions: Chat and Stream Chat -------------------------- #

    @llm_retry_decorator
    def _chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        """
        Sends chat messages to the API and returns the response.
        """
        client = self._get_client()
        message_dicts = to_openai_message_dicts(messages)
        
        if self.reuse_client:
            response = client.chat.completions.create(
                messages=message_dicts,
                stream=False,
                **self._get_model_kwargs(**kwargs),
            )
        else:
            with client:
                response = client.chat.completions.create(
                    messages=message_dicts,
                    stream=False,
                    **self._get_model_kwargs(**kwargs),
                )
        openai_message = response.choices[0].message
        message = from_openai_message(openai_message)

        return ChatResponse(
            message=message,
            raw=response,
            additional_kwargs=self._get_response_token_counts(response),
        )


    @llm_retry_decorator
    def _stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        """
        Streams chat completions from the API and yields response chunks.
        """
        client = self._get_client()
        message_dicts = to_openai_message_dicts(messages)

        def gen() -> ChatResponseGen:
            content = ""

            for response in client.chat.completions.create(
                messages=message_dicts,
                **self._get_model_kwargs(stream=True, **kwargs),
            ):
                response = cast(ChatCompletionChunk, response)
                if len(response.choices) > 0:
                    delta = response.choices[0].delta
                else:
                    delta = ChoiceDelta()

                # update using deltas
                role = delta.role or MessageRole.ASSISTANT
                content_delta = delta.content or ""
                content += content_delta

                additional_kwargs = {}

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                        additional_kwargs=additional_kwargs,
                    ),
                    delta=content_delta,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()
    
    
    # ------------------------ Class Functions: Complete and Stream Complete -------------------------- #

    @llm_retry_decorator
    def _complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        client = self._get_client()
        all_kwargs = self._get_model_kwargs(**kwargs)

        if self.reuse_client:
            response = client.completions.create(
                prompt=prompt,
                stream=False,
                **all_kwargs,
            )
        else:
            with client:
                response = client.completions.create(
                    prompt=prompt,
                    stream=False,
                    **all_kwargs,
                )
        text = response.choices[0].text

        return CompletionResponse(
            text=text,
            raw=response,
            additional_kwargs=self._get_response_token_counts(response),
            )
        

    @llm_retry_decorator
    def _stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        """
        Streams text completion from the API and yields response chunks.
        """
        client = self._get_client()
        all_kwargs = self._get_model_kwargs(stream=True, **kwargs)

        def gen() -> CompletionResponseGen:
            text = ""
            for response in client.completions.create(
                prompt=prompt,
                **all_kwargs,
            ):
                if len(response.choices) > 0:
                    delta = response.choices[0].text
                    if delta is None:
                        delta = ""
                else:
                    delta = ""
                text += delta
                
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()
    
    # ------------------------ Class Function: Get response token count -------------------------- #

    def _get_response_token_counts(self, raw_response: Any) -> dict:
        """Get the token usage reported by the response."""
        if hasattr(raw_response, "usage"):
            try:
                prompt_tokens = raw_response.usage.prompt_tokens
                completion_tokens = raw_response.usage.completion_tokens
                total_tokens = raw_response.usage.total_tokens
            except AttributeError:
                return {}
        elif isinstance(raw_response, dict):
            usage = raw_response.get("usage", {})
            # NOTE: other model providers that use the OpenAI client may not report usage
            if usage is None:
                return {}
            # Backwards compatibility with old dict type
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)
        else:
            return {}

        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        }


    
    # ------------------------ Async Endpoints -------------------------- #
    
    # ------------------------ Base LLM Class Functions ---------------------- #
    
    @llm_chat_callback()
    async def achat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponse:
        achat_fn: Callable[..., Awaitable[ChatResponse]]
        if self._use_chat_completions(kwargs):
            achat_fn = self._achat
        else:
            achat_fn = acompletion_to_chat_decorator(self._acomplete)
        return await achat_fn(messages, **kwargs)
    

    @llm_chat_callback()
    async def astream_chat(
        self,
        messages: Sequence[ChatMessage],
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        astream_chat_fn: Callable[..., Awaitable[ChatResponseAsyncGen]]
        if self._use_chat_completions(kwargs):
            astream_chat_fn = self._astream_chat
        else:
            astream_chat_fn = astream_completion_to_chat_decorator(
                self._astream_complete
            )
        return await astream_chat_fn(messages, **kwargs)


    @llm_completion_callback()
    async def acomplete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        if self._use_chat_completions(kwargs):
            acomplete_fn = achat_to_completion_decorator(self._achat)
        else:
            acomplete_fn = self._acomplete
        return await acomplete_fn(prompt, **kwargs)


    @llm_completion_callback()
    async def astream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        if self._use_chat_completions(kwargs):
            astream_complete_fn = astream_chat_to_completion_decorator(
                self._astream_chat
            )
        else:
            astream_complete_fn = self._astream_complete
        return await astream_complete_fn(prompt, **kwargs)
    
    

    # --------- Class Functions: Async Chat and Async Stream Chat ------------- #
    
    @llm_retry_decorator
    async def _achat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponse:
        """
        Sends asynchronous chat messages to the API and returns the response.
        """
        aclient = self._get_aclient()
        message_dicts = to_openai_message_dicts(messages)

        if self.reuse_client:
            response = await aclient.chat.completions.create(
                messages=message_dicts, stream=False, **self._get_model_kwargs(**kwargs)
            )
        else:
            async with aclient:
                response = await aclient.chat.completions.create(
                    messages=message_dicts,
                    stream=False,
                    **self._get_model_kwargs(**kwargs),
                )

        openai_message = response.choices[0].message
        message = from_openai_message(openai_message)

        return ChatResponse(
            message=message,
            raw=response,
            additional_kwargs=self._get_response_token_counts(response),
        )
        


    @llm_retry_decorator
    async def _astream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseAsyncGen:
        """
        Streams asynchronous chat completions from the API and yields response chunks.
        """
        aclient = self._get_aclient()
        message_dicts = to_openai_message_dicts(messages)

        async def gen() -> ChatResponseAsyncGen:
            content = ""

            first_chat_chunk = True
            async for response in await aclient.chat.completions.create(
                messages=message_dicts,
                **self._get_model_kwargs(stream=True, **kwargs),
            ):
                response = cast(ChatCompletionChunk, response)
                if len(response.choices) > 0:
                    # check if the first chunk has neither content nor tool_calls
                    # this happens when 1106 models end up calling multiple tools
                    if (
                        first_chat_chunk
                        and response.choices[0].delta.content is None
                    ):
                        first_chat_chunk = False
                        continue
                    delta = response.choices[0].delta
                else:
                    delta = ChoiceDelta()
                first_chat_chunk = False

                # update using deltas
                role = delta.role or MessageRole.ASSISTANT
                content_delta = delta.content or ""
                content += content_delta

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                    ),
                    delta=content_delta,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()
    
    
    # ------- Class Functions: Async Completion and Async Stream Completion -------- #

    @llm_retry_decorator
    async def _acomplete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        """
        Asynchronously completes a prompt using the API and returns the response.
        """
        aclient = self._get_aclient()
        all_kwargs = self._get_model_kwargs(**kwargs)

        if self.reuse_client:
            response = await aclient.completions.create(
                prompt=prompt,
                stream=False,
                **all_kwargs,
            )
        else:
            async with aclient:
                response = await aclient.completions.create(
                    prompt=prompt,
                    stream=False,
                    **all_kwargs,
                )

        text = response.choices[0].text
        
        return CompletionResponse(
            text=text,
            raw=response,
            additional_kwargs=self._get_response_token_counts(response),
        )
        

    @llm_retry_decorator
    async def _astream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseAsyncGen:
        """
        Streams asynchronous text completions from the API and yields response chunks.
        """
        aclient = self._get_aclient()
        all_kwargs = self._get_model_kwargs(stream=True, **kwargs)

        async def gen() -> CompletionResponseAsyncGen:
            text = ""
            async for response in await aclient.completions.create(
                prompt=prompt,
                **all_kwargs,
            ):
                if len(response.choices) > 0:
                    delta = response.choices[0].text
                    if delta is None:
                        delta = ""
                else:
                    delta = ""
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    raw=response,
                    additional_kwargs=self._get_response_token_counts(response),
                )

        return gen()
    
    
    # ------------------ Function Calling LLM Methods ------------------------ #
    # ----------------- Class Functions: Prepare Chat with Tools ---------------- #
    def _prepare_chat_with_tools(
        self,
        tools: Sequence[FunctionTool],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        
        tool_specs: List[Dict[str, Any]] = []
        
        # Format each tool to openai JSON format
        for tool in tools:
            openai_tool = tool.metadata.to_openai_tool()
            self._remove_title_key(openai_tool)
            tool_specs.append(openai_tool)

        if isinstance(user_msg, str):
            user_msg = ChatMessage(role=MessageRole.USER, content=user_msg)

        tool_calling_system_msg = ChatMessage( 
                role="system",  
                content=self._generate_tool_calling_prompt(
                    function_json_list=tool_specs,
                )
            )
        messages = [tool_calling_system_msg]
        
        if chat_history:
            messages.extend(chat_history)
            
        if user_msg:
                messages.append(user_msg)

        return {
            "messages": messages,
            **kwargs,
        }
        
    # -------------- Function Calling LLM: Chat with Tools --------------- #

    def chat_with_tools(
        self,
        tools: Sequence[FunctionTool],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> ChatResponse:
        chat_kwargs = self._prepare_chat_with_tools(
            tools,
            user_msg=user_msg,
            chat_history=chat_history,
            verbose=verbose,
            allow_parallel_tool_calls=allow_parallel_tool_calls,
            **kwargs,
        )
            
        response = self.chat(
            **chat_kwargs,
        )
        
        
        content = response.message.content
        tool_calls = self._extract_function_call_from_message(
            content=content,
        )
        
        if tool_calls:
            response.message.content = "" 
            
        response.message.additional_kwargs["tool_calls"] = self._to_openai_completionMessageToolCall(
            tool_calls=tool_calls,
        )
        
        return self._validate_chat_with_tools_response(
            response,
            tools,
            allow_parallel_tool_calls=allow_parallel_tool_calls,
            **kwargs,
        )

    async def achat_with_tools(
        self,
        tools: Sequence["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> ChatResponse:
        chat_kwargs = self._prepare_chat_with_tools(
            tools,
            user_msg=user_msg,
            chat_history=chat_history,
            verbose=verbose,
            allow_parallel_tool_calls=allow_parallel_tool_calls,
            **kwargs,
        )
        response = await self.achat(**chat_kwargs)
        

        content = response.message.content
        tool_calls = self._extract_function_call_from_message(
            content=content,
        )
        
        if tool_calls:
            response.message.content = "" 
            
        response.message.additional_kwargs["tool_calls"] = self._to_openai_completionMessageToolCall(
            tool_calls=tool_calls,
        )
        
        
        return self._validate_chat_with_tools_response(
            response,
            tools,
            allow_parallel_tool_calls=allow_parallel_tool_calls,
            **kwargs,
        )

    # -------------- Function Calling LLM: Stream Chat with Tools  --------------- #

    # TODO: Implement actual streaming
    

    def stream_chat_with_tools(
        self,
        tools: Sequence["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> ChatResponseGen:
        """Stream chat with function calling."""
        chat_kwargs = self._prepare_chat_with_tools(
            tools,
            user_msg=user_msg,
            chat_history=chat_history,
            verbose=verbose,
            allow_parallel_tool_calls=allow_parallel_tool_calls,
            **kwargs,
        )
        raise(NotImplementedError("Stream chat with tools not implemented"))


    async def astream_chat_with_tools(
        self,
        tools: Sequence["BaseTool"],
        user_msg: Optional[Union[str, ChatMessage]] = None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        allow_parallel_tool_calls: bool = False,
        **kwargs: Any,
    ) -> ChatResponseAsyncGen:
        raise(NotImplementedError("A stream chat with tools not implemented"))
    

    # --------- Function Calling Functions:  Get tool calls from response ------------- #

    def get_tool_calls_from_response(
        self,
        response: ChatResponse,
        error_on_no_tool_call: bool = True,
        **kwargs: Any,
    ) -> List[ToolSelection]:
        """Predict and call the tool."""
        tool_calls = response.message.additional_kwargs.get("tool_calls")

        tool_selections = []
        for tool_call in tool_calls:
            if not isinstance(tool_call, get_args(OpenAIToolCall)):
                raise ValueError("Invalid tool_call object")
            if tool_call.type != "function":
                raise ValueError("Invalid tool type. Unsupported by OpenAI")

            # this should handle both complete and partial jsons
            try:
                argument_dict = parse_partial_json(tool_call.function.arguments)
            except ValueError:
                argument_dict = {}

            tool_selections.append(
                ToolSelection(
                    tool_id=tool_call.id,
                    tool_name=tool_call.function.name,
                    tool_kwargs=argument_dict,
                )
            )

        return tool_selections
    
    

    # --------- Utils for LLM function calling ------------- #
    
    def _remove_title_key(self, d):
        """Function to recursively remove all "title" keys from the dictionary"""

        if isinstance(d, dict):
            if "title" in d:
                del d["title"]  # Remove the "title" key
            # Recursively check nested dictionaries
            for key in d:
                self._remove_title_key(d[key])
        elif isinstance(d, list):
            # If value is a list, check each element
            for item in d:
                self._remove_title_key(item)
                
                
    def _generate_tool_calling_prompt(
        self, 
        function_json_list: List[Dict[str, Any]]
    ) -> str:
        """Generate a system prompt for selecting and calling functions in JSON format."""
        function_json_text = json.dumps(function_json_list, indent=4)
        message = f"""You are a helpful assistant equipped with a bank of callable functions.

    Your task is to respond to user requests by selecting the appropriate function from the available list and generating a function call in JSON format with its required arguments.

    Instructions:

    1. Always respond with a JSON object that includes:

    - "name": the name of the function to call.
    - "parameters": a dictionary mapping argument names to their respective values.

    2. Do not use variables in the parameters. Instead, provide explicit values directly in the JSON.

    3. If any required parameters for a function are missing or unclear, ask the user for the specific details to complete the function call. Use concise, clear questions to gather the necessary information.

    4. The JSON format for the function call should look like this: 
    ```json
    {{
        "name": "<function_name>",
        "parameters": {{
        "<argument_name>": <argument_value>,
        ...
        }}
    }}

    Available functions to call: 
    {function_json_text}"""

        return message
    
    
    def _extract_function_call_from_message(
        self, 
        content: str
    ) -> List[Dict]:
        """Extract and parse a JSON function call from a string."""
        tool_calls_list = []
        # Iterate through all matches and load them as JSON
        for match in re.finditer(r'```json[^\n]*\n(.+?)```', content, re.S):
            try:
                tool_calls = json.loads(match.group(1))
                tool_calls_list.append(tool_calls)
            except json.JSONDecodeError as e:
                print(f"Error: {e.msg}")
        return tool_calls_list


    
    def _to_openai_completionMessageToolCall(
        self, 
        tool_calls: List[Dict],
    ) -> List[ChatCompletionMessageToolCall]:        
        """
        Convert a list of tool calls represented as dictionaries into a list of
        ChatCompletionMessageToolCall objects.
        """
        tool_calls_converted = []
        
        for tool in tool_calls:
            id = f"call_{uuid.uuid4()}"
            function = Function(
                arguments=json.dumps(tool.get("parameters", "")),
                name=tool.get("name", ""),
            )
            type = "function"
            
            tool_calls_converted.append(
                ChatCompletionMessageToolCall(
                    id=id,
                    function=function, 
                    type=type,
                )
            )
            
        return tool_calls_converted
        
        
        
        
        
        