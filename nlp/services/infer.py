import logging
import spacy
from spacy.tokens import Doc
from common.constants import MODEL_PATH
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
    def __init__(self, **spacy_kwargs) -> None:
        try:
            self.model = spacy.load(MODEL_PATH, **spacy_kwargs)
        except Exception as e:
            msg = f"Failed to load spaCy model from path: `{MODEL_PATH}`"
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
        )

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