from dataclasses import dataclass
from .enums import ParamKeyEnum, ParamValueEnum


@dataclass
class ParamDict:
    params: dict[ParamKeyEnum, ParamValueEnum]
