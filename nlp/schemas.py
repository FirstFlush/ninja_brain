from pydantic import BaseModel
from typing import Any
from nlp.dataclasses import EntitySpan
from .enums import MLModelEnum


class EntityPredictionData(BaseModel):
    sms_id: int
    elapsed_ms: int
    version: str
    ml_model_enum: MLModelEnum
    entities: list[EntitySpan]


class PredictionRequest(BaseModel):
    text: str
    id: int
    
    
class PredictionResponse(BaseModel):
    entities: list[dict[str, Any]]