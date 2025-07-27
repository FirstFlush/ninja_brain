class ModelLoadError(Exception):
    """Raised when the NLP model fails to load."""
    pass


class InferenceError(Exception):
    """Raised when the NLP model fails to process input text."""
    pass