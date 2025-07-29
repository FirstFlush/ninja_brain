from dataclasses import dataclass
from .enums import MLModelEnum

@dataclass
class EntitySpan:
    label: str
    text: str
    start: int
    end: int

@dataclass
class InferredEntities:
    text: str
    ml_model_enum: MLModelEnum
    version: str
    entities: list[EntitySpan]
