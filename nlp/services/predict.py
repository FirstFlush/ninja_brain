from django.conf import settings
import logging
from common.utils.timer import time_ms
from .infer import EntityInferenceService
from .persist import EntityPersistenceService
from ..dataclasses import InferredEntities
from ..enums import MLModelEnum
from ..errors.inference_errors import ModelLoadError, InferenceError
from ..models import EntityPrediction
from ..schemas import EntityPredictionData, PredictionRequest, PredictionResponse


logger = logging.getLogger(__name__)


class EntityPredictionService:
    
    def __init__(
            self, 
            request_data: PredictionRequest, 
            model_name: str = settings.ML_MODEL,
    ):
        self.request_data = request_data
        self.ml_model_enum = self._ml_model_enum(model_name)

    def predict(self) -> PredictionResponse:
        infer_service = EntityInferenceService(ml_model=self.ml_model_enum)
        inferred_data, elapsed_ms = time_ms(infer_service.infer, text=self.request_data.text)
        prediction_data = self._prediction_data(inferred_data, elapsed_ms)
        persistence_service = EntityPersistenceService(prediction_data)
        entity_prediction = persistence_service.save()
            
        return self._build_response(entity_prediction)

    def _build_response(self, prediction: EntityPrediction) -> PredictionResponse:
        return PredictionResponse(
            entities = prediction.extracted_entities
        )

    def _prediction_data(self, inferred_data: InferredEntities, elapsed_ms: int) -> EntityPredictionData:
        return EntityPredictionData(
            sms_id = self.request_data.id,
            elapsed_ms = elapsed_ms,
            version = inferred_data.version,
            ml_model_enum = inferred_data.ml_model_enum,
            entities = inferred_data.entities,
        )
        
    def _ml_model_enum(self, model_name: str) -> MLModelEnum:
        try:
            return MLModelEnum(model_name)
        except ValueError as e:
            msg = f"{self.__class__.__name__} received invalid model_name: {model_name}. Is this a typo?"
            logger.error(msg, exc_info=True)
            raise ModelLoadError(msg) from e