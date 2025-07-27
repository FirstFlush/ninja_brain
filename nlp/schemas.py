from pydantic import BaseModel


class PredictionInput(BaseModel):
    text: str
    id: int