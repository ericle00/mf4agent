from typing import Optional
from abc import ABCMeta


class ResponseErrorBase(Exception, metaclass=ABCMeta):

    def __init__(
        self, identifier: str, message: str, hint: Optional[str] = None
    ) -> None:
        """Initialize the error.

        Args:
            identifier (str): The prefix string that identifies the error
            message (str): The message to send back to the user
            hint (str, optional): Provide a hint to the user that can fix the error. Defaults to None.
        """

        self._identifier = identifier

        # Initialize the exception with a hint or not
        if hint is None:
            super().__init__(message)

        else:
            super().__init__(f"{message} Hint: {hint}")

    def check(self, response: str) -> None:
        """Check if the response starts with the error identifier.

        Args:
            response (str): The string response from the encoder/decoder

        Raises:
            self: An error, defined in the subclasses
        """

        if response.startswith(self._identifier):
            raise self


class CudaOutOfMemory(ResponseErrorBase):

    def __init__(self) -> None:

        identifier = "[Inference error] CUDA out of memory"

        message = "The server has run out of GPU VRAM."

        hint = (
            "Ask someone from the Core ML team to restart the service. "
            "We are sorry about the inconvenience."
        )

        super().__init__(identifier, message, hint)


class EncoderNotInitialized(ResponseErrorBase):

    def __init__(self) -> None:

        identifier = '"[Server Error] Encoder is not initialized."'

        message = "The encoder model is not initialized on this server."

        hint = (
            "Check that the IP and/or PORT for the model are correct. "
        )

        super().__init__(identifier, message, hint)
