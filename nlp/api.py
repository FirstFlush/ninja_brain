from ninja import Router
from ninja.responses import Response
from django.http import HttpRequest
import logging
from .schemas import PredictionRequest
from .services.predict import EntityPredictionService
from common.responses.builders import ApiResponseBuilder
from common.responses.schemas import ApiResponse
from nlp.schemas import PredictionResponse

logger = logging.getLogger(__name__)
router = Router()

@router.post("/predict")
def predict(request: HttpRequest, data: PredictionRequest):
    
    prediction_service = EntityPredictionService(request_data=data)
    prediction_response = prediction_service.predict()

    api_response = ApiResponseBuilder.from_data(data=prediction_response)
    return Response(api_response)