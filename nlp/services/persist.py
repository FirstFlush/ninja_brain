from dataclasses import asdict
import logging
from typing import Any
from common.constants import DB_WRITE_EXCEPTIONS 
from ..errors.persistence_errors import PersistenceError
from ..models import EntityPrediction
from ..schemas import EntityPredictionData

logger = logging.getLogger(__name__)

class EntityPersistenceService:
    
    def __init__(self, prediction_data: EntityPredictionData):
        self.data = prediction_data

    def save(self) -> EntityPrediction:
        try:
            return EntityPrediction.objects.create(
                sms_id=self.data.sms_id,
                response_time_ms=self.data.elapsed_ms,
                entities=self._serialize_entities(),
                version=self.data.version,
            )
        except DB_WRITE_EXCEPTIONS as e:
            msg = f"Failed to persist EntityPrediction for sms_id `{self.data.sms_id}`"
            logger.error(msg, exc_info=True)
            raise PersistenceError(msg) from e
        
    def _serialize_entities(self) -> list[dict[str, Any]]:
        return [asdict(ent) for ent in self.data.entities]