from typing import AnyStr
from agent.abstract.protocol import Protocol

class Protocol(Protocol):
    """
    My custom protocol class.
    """
    def __init__(self) -> None:
        """
        Initialize the protocol.
        """
        pass
    
    def format(self, instruction: AnyStr, history: AnyStr) -> AnyStr:
        """
        Format the instruction and history.

        Parameters:
            instruction (AnyStr): Instruction to be formatted.
            history (AnyStr): History to be formatted.

        Returns:
            AnyStr: Formatted instruction and history.
        """
        pass
    
    def parse(self, generated_text: AnyStr) -> AnyStr:
        """
        Parse the generated text.

        Parameters:
            generated_text (AnyStr): Text to be parsed.

        Returns:
            AnyStr: Parsed text.
        """
        pass