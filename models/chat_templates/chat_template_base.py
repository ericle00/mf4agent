from abc import ABC, abstractmethod

class ChatTemplateBase(ABC):
    def __init__(self) -> None:
        """
        Initialize the ChatTemplateBase class.
        """
        super().__init__()
    
    @abstractmethod
    def process_messages(self, messages: list[dict]) -> str:
        """
        Process a list of messages, each containing a role and content, 
        and apply a chat template to generate a formatted string.

        Args:
            messages (list[dict[str, str]]): A list of dictionaries where each dictionary
            contains 'role' and 'content' keys.

        Returns:
            str: The formatted chat template string.
        """
        pass
    
def system_message(message: str) -> dict:
    """
    Create a dictionary representing a system message.

    Args:
    message (str): The content of the system message.

    Returns:
    Dict[str, str]: A dictionary with the role set to 'system' and the content set to the provided message.
    """
    return {"role": "system", "content": message}

def user_message(message: str) -> dict:
    """
    Create a dictionary representing a user message.

    Args:
    message (str): The content of the user message.

    Returns:
    Dict[str, str]: A dictionary with the role set to 'user' and the content set to the provided message.
    """
    return {"role": "user", "content": message}

def assistant_message(message: str) -> dict:
    """
    Create a dictionary representing an assistant message.

    Args:
    message (str): The content of the assistant message.

    Returns:
    Dict[str, str]: A dictionary with the role set to 'assistant' and the content set to the provided message.
    """
    return {"role": "assistant", "content": message}

