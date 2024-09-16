from volvo_dev.utils.colored_text import print_prompt_after_formatting
from volvo_dev.chat_templates.chat_template_base import ChatTemplateBase

class CodeLLama2PhindChatTemplate(ChatTemplateBase):
    def __init__(self) -> None:
        """
        Initialize the CodeLLama2PhindChatTemplate class.
        https://huggingface.co/Phind/Phind-CodeLlama-34B-v2
        """
        super().__init__()
            
    def process_messages(self, 
                         messages: list[dict], 
                         add_generation_prompt: bool=True,
                         verbose: bool = True):
        """
        Process a list of messages to create a formatted chat conversation string.

        Args:
            messages (list[dict[str, str]]): A list of message dictionaries, each containing "role" and "content".
            add_generation_prompt (bool, optional): Whether to add a generation prompt for the assistant. Defaults to True.
            verbose (bool): Print the reformatted prompt in terminal. Defaults to True.

        Returns:
            str: The formatted chat conversation string.

        Raises:
            Exception: If the roles in the conversation do not alternate correctly.
        """
        # Process system message if present
        if messages[0]["role"] == "system":
            system_message = messages[0]["content"].strip() + "\n\n"
            messages = messages[1:]
        else:
            system_message = ""

        # Initialize formatted message with bos_token and system_message
        formatted_messages = f"### System prompt\n{system_message}\n\n "

        # Process each message
        for i, message in enumerate(messages):
            # Check if roles alternate correctly
            if (message["role"] == "user") != (i % 2 == 0):
                raise Exception("Conversation roles must alternate user/assistant/user/assistant/...")

            # Format the messages
            if message["role"] == "user":
                formatted_messages += "### User Message:\n" + message["content"].strip() + "\n\n"
            elif message["role"] == "assistant":
                formatted_messages += "### Assistant:\n" + message["content"].strip() + "\n\n"

        # Optionally add generation prompt
        if add_generation_prompt:
            formatted_messages += "### Assistant:\n"
        
        # Print reformatted prompt
        if verbose:
            print_prompt_after_formatting(formatted_messages)
            
        return formatted_messages