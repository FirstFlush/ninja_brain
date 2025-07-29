from http import HTTPStatus
from ninja import Router
from ninja.responses import Response
from django.http import HttpRequest
import logging
from .schemas import PredictionRequest
from .services.predict import EntityPredictionService
from common.responses.builders import ApiSuccessResponseBuilder, ApiErrorResponseBuilder
from common.responses.schemas import ApiSuccessResponse, ApiErrorResponse
from nlp.schemas import PredictionResponse

logger = logging.getLogger(__name__)
router = Router()

@router.post("/predict")
def predict(request: HttpRequest, data: PredictionRequest):
    
    prediction_service = EntityPredictionService(request_data=data)
    prediction_response = prediction_service.predict()

    response_builder = ApiSuccessResponseBuilder(data=prediction_response)
    
    try:
        _ = 1 / 0
        ...
    except Exception as e:
        response_builder = ApiErrorResponseBuilder(error=e, status=HTTPStatus.OK)

    api_response = response_builder.build()
    api_response.payload
    return Response(api_response)