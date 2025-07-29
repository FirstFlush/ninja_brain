from ninja import Router
from django.http import HttpRequest
import logging
from .schemas import PredictionRequest
from .services.predict import EntityPredictionService

logger = logging.getLogger(__name__)
router = Router()

@router.post("/predict")
def predict(request: HttpRequest, data: PredictionRequest):
    
    prediction_service = EntityPredictionService(request_data=data)
    prediction_service.predict()



    return {"entities": []} 