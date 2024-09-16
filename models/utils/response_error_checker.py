from enum import Enum

from volvo_dev.utils.exceptions import CudaOutOfMemory, EncoderNotInitialized


class _AvailableErrors(Enum):
    CUDA_OUT_OF_MEMORY = CudaOutOfMemory()

    ENCODER_NOT_INITIALIZED = EncoderNotInitialized()


class ResponseErrorChecker:
    """
    This class is used to check for errors in the response from the encoder and decoder models.
    Errors could for example be `Cuda out of memory`, or `Encoder is not initialized.`.
    Both of these errors are written in clear text and sent back to the user as nothing happened.
    So this class is putting a layer of "protection", between the model and the user.

    This class is meant to be used without "initializing" it.
    (Contains only static methods)
    """

    @staticmethod
    def check(response: str) -> None:
        """
        Check the response from the LLM against some known errors.
        The errors are presented in the response as strings.
        If no exceptions are thrown, then there are no errors in the response.

        Args:
            response (str): The string response from the encoder/decoder

        Raises:
            CudaOutOfMemory: If the server ran out of VRAM
            EncoderNotInitialized: If the encoder is not initialized
        """

        for errors in _AvailableErrors:
            errors.value.check(response)