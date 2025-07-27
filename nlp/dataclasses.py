from dataclasses import dataclass

@dataclass
class EntitySpan:
    label: str
    text: str
    start: int
    end: int

@dataclass
class InferredEntities:
    text: str
    entities: list[EntitySpan]
