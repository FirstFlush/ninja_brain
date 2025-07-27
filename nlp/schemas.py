from pydantic import BaseModel
from nlp.dataclasses import EntitySpan


class EntityPredictionData(BaseModel):
    sms_id: int
    elapsed_ms: int
    version: str
    entities: list[EntitySpan]


class PredictionInput(BaseModel):
    text: str
    id: int