from ninja import Router
from django.http import HttpRequest
import logging
from .schemas import PredictionInput
from .services.infer import EntityInferenceService

logger = logging.getLogger(__name__)
router = Router()

@router.post("/predict")
def predict(request: HttpRequest, data: PredictionInput):
        
    service = EntityInferenceService()
    inferred_entities = service.infer(text=data.text)

    return {"entities": []} 