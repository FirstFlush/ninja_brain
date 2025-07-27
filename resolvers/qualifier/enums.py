from enum import Enum


class ParamEnum(Enum):
    """Abstract parent for all enums related to SMS inquiry params."""
    pass


class ParamKeyEnum(ParamEnum):
    """
    Defines the keys used in the resource filter query's kwargs dict
    """

class ParamValueEnum(ParamEnum):
    """Defines the possible values for filtering parameters."""
    pass


class BooleanParamValue(ParamValueEnum):
    TRUE = True
    FALSE = False