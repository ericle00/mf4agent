from abc import ABC, abstractmethod
from typing import AnyStr

class Protocol(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def format(instruction:AnyStr, history:AnyStr) -> AnyStr:
        """Format the instruction to match the requirement of the LLM model.

        Args:
            instruction (AnyStr): the instruction you want to give to the LLM model. 
            history (AnyStr): the history of the chat you want to use.
        
        Return:
            formated_instruction (AnyStr)
        """
        pass
    
    @abstractmethod
    def parse(generated_text:AnyStr):
        """Parse the generated text given by the LLM model and take out the answer.

        Args:
            generated_text (AnyStr): the genereated text taken from the response of the LLM model.
        """
        pass