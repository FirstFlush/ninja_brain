import logging
import spacy
from spacy.tokens import Doc
from ..enums import MLModelEnum
from ..dataclasses import InferredEntities, EntitySpan
from ..errors.inference_errors import ModelLoadError, InferenceError

logger = logging.getLogger(__name__)


class EntityInferenceService:
    """
    Performs named entity recognition on input text using a pre-trained spaCy model.

    Raises:
        ModelLoadError: If the spaCy model fails to load on initialization.
        InferenceError: If input is invalid or the model fails during inference.
    """
    def __init__(self, ml_model: MLModelEnum, **spacy_kwargs) -> None:
        self.model_enum = ml_model
        try:
            self.model = spacy.load(self.model_enum.value, **spacy_kwargs)
        except Exception as e:
            msg = f"Failed to load spaCy model from path: `{self.model_enum.value}`"
            logger.error(msg, exc_info=True)
            raise ModelLoadError(msg) from e

    def infer(self, text: str) -> InferredEntities:
        self._validate_input(text)
        doc = self._run_model(text)
        entities = [
            EntitySpan(
                label=ent.label_,
                text=ent.text,
                start=ent.start_char,
                end=ent.end_char,
            ) for ent in doc.ents
        ]
        return InferredEntities(
            text = text,
            entities = entities,
            version=self._version(),
            ml_model_enum=self.model_enum,
        )

    def _version(self) -> str:
        return self.model.meta.get("version", "unknown")

    def _validate_input(self, text: str):
        if not isinstance(text, str):
            msg = f"Expected 'text' parameter to be a string, got `{type(text)}`"
            logger.error(msg)
            raise InferenceError(msg)
    
    def _run_model(self, text: str) -> Doc:
        try:
            return self.model(text)
        except Exception as e:
            msg = f"spaCy model failed to process text: `{text}`"
            logger.error(msg, exc_info=True)
            raise InferenceError(msg) from e