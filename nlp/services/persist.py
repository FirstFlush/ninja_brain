from dataclasses import asdict
from django.db import transaction
import logging
from typing import Any
from common.constants import DB_WRITE_EXCEPTIONS 
from ..errors.persistence_errors import PersistenceError
from ..models import EntityPrediction, MLModel
from ..schemas import EntityPredictionData

logger = logging.getLogger(__name__)

class EntityPersistenceService:
    """
    Handles saving an EntityPrediction to the database
    
    Raises:
        PersistenceError: If the database write fails.
    """
    def __init__(self, prediction_data: EntityPredictionData):
        self.data = prediction_data

    def _get_or_create_ml_model(self) -> MLModel:
        try:
            ml_model, created = MLModel.objects.get_or_create(
                name=self.data.ml_model_enum,
                version=self.data.version
            )
        except DB_WRITE_EXCEPTIONS as e:
            msg = f"Failed to get or create MLModel instance with name `{self.data.ml_model_enum}` and version `{self.data.version}`"
            logger.error(msg, exc_info=True)
            raise PersistenceError(msg) from e
        else:            
            logger.debug(f"Retrieved MLModel object: `{ml_model}`, created: `{created}`")
            return ml_model

    def save(self) -> EntityPrediction:        
        with transaction.atomic():
            ml_model = self._get_or_create_ml_model()
            prediction = self._create_prediction(ml_model)
        return prediction
    
    def _create_prediction(self, ml_model: MLModel) -> EntityPrediction:
        try:
            prediction = EntityPrediction.objects.create(
                ml_model=ml_model,
                sms_id=self.data.sms_id,
                response_time_ms=self.data.elapsed_ms,
                extracted_entities=self._serialize_entities(),
            )
        except DB_WRITE_EXCEPTIONS as e:
            msg = f"Failed to persist EntityPrediction for sms_id `{self.data.sms_id}`"
            logger.error(msg, exc_info=True)
            raise PersistenceError(msg) from e
        else:
            logger.debug(f"Created EntityPrediction: `{prediction}`")
            return prediction
        
    def _serialize_entities(self) -> list[dict[str, Any]]:
        return [asdict(ent) for ent in self.data.entities]