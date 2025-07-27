from dataclasses import dataclass
from .enums import ResourceEnum


@dataclass
class ResolvedResource:
    resource: ResourceEnum