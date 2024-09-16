from volvo_dev.utils.colored_text import print_prompt_after_formatting
from volvo_dev.chat_templates.chat_template_base import ChatTemplateBase

class Mixtral8x7BChatTemplate(ChatTemplateBase):
    def __init__(self) -> None:
        """
        Initialize the MixtralChatTemplate class.
        https://community.aws/content/2dFNOnLVQRhyrOrMsloofnW0ckZ/how-to-prompt-mistral-ai-models-and-why
        https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1
        """
        super().__init__()
        
    def process_messages(self, 
                         messages: list[dict],
                         primer: str = "",
                         verbose: bool = True) -> str:
        """
        Process a list of messages to create a formatted chat conversation string.

        Args:
            messages (list[dict[str, str]]): A list of message dictionaries, each containing "role" and "content".
            verbose (bool): Print the reformatted prompt in terminal. Defaults to True.

        Returns:
            str: The formatted chat conversation string.

        Raises:
            Exception: If the roles in the conversation do not alternate correctly.
        """
        bos_token: str ="<s>"
        eos_token: str = "</s>"
                        
        if messages[0]["role"] == "system":
            system_message = messages[0]["content"].strip() + "\n\n"
            messages = messages[1:]
        else:
            system_message = ""

        formatted_messages = bos_token + system_message
        for i, message in enumerate(messages):
            if (message["role"] == "user") != (i % 2 == 0):
                raise Exception("Conversation roles must alternate user/assistant/user/assistant/...")

            if message["role"] == "user":
                formatted_messages += "[INST] " + message["content"].strip() + " [/INST]"
            elif message["role"] == "assistant":
                formatted_messages += message["content"].strip() + eos_token + " "
                
        if primer:
            formatted_messages += f" {primer}"
            
        # Print reformatted prompt
        if verbose:
            print_prompt_after_formatting(formatted_messages)
            
        return formatted_messages