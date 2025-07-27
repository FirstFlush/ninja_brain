from common.errors import NinjaBrainException


class PersistenceError(NinjaBrainException):
    """Raised when an EntityPrediction fails to save to the DB"""
    pass