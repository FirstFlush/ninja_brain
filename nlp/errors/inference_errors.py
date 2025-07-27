from common.errors import NinjaBrainException


class ModelLoadError(NinjaBrainException):
    """Raised when the NLP model fails to load."""
    pass


class InferenceError(NinjaBrainException):
    """Raised when the NLP model fails to process input text."""
    pass