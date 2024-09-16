from volvo_dev.utils.colored_text import print_prompt_after_formatting
from volvo_dev.chat_templates.chat_template_base import ChatTemplateBase

class LLama31InstructChatTemplate(ChatTemplateBase):
    def __init__(self) -> None:
        """
        Initialize the LLama 3.1 version Instruct class chat template.
        https://llama.meta.com/docs/model-cards-and-prompt-formats/llama3_1/
        """
        super().__init__()
        
            
    def process_messages(self, 
                         messages: list[dict], 
                         add_generation_prompt:bool=True,
                         verbose: bool = True):
        
        BOT_TOKEN = "<|begin_of_text|>"
        START_HEADER_ID_TOKEN, END_HEADER_ID_TOKEN = "<|start_header_id|>", "<|end_header_id|>"
        END_OF_MESSAGE_ID, END_OF_TOKEN_ID = "<|eom_id|>", "<|eot_id|>"
        FINE_TUNE_RIGHT_PAD_ID, PYTHON_TAG = "<|finetune_right_pad_id|>", "<|python_tag|>"
        
        # Determine the offset based on the first message role
        offset = 1 if messages[0]['role'] == 'system' else 0

        output = BOT_TOKEN
        

        for index, message in enumerate(messages):
            # Check if the roles alternate correctly
            if (message['role'] == 'user') != (index % 2 == offset):
                raise Exception('Conversation roles must alternate user/assistant/user/assistant/...')

            output += START_HEADER_ID_TOKEN + message["role"] + END_HEADER_ID_TOKEN + "\n\n"
            output += message["content"] + END_OF_TOKEN_ID
                

        # Add generation prompt if required
        if add_generation_prompt:
            output += START_HEADER_ID_TOKEN + "assistant" + END_HEADER_ID_TOKEN

        # Print reformatted prompt
        if verbose:
            print_prompt_after_formatting(output)
            
        return output
