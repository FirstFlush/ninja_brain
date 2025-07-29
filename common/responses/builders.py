from abc import ABC, abstractmethod
from datetime import datetime, timezone
from http import HTTPStatus
import logging
from typing import Any, Generic, TypeVar
from .errors import ApiPayloadBuilderError, ApiResponseBuilderError
from .schemas import SuccessPayload, ErrorPayload, ErrorPayloadData, ApiSuccessResponse, ApiErrorResponse, ResponseMeta


logger = logging.getLogger(__name__)
T = TypeVar("T")


class ApiResponseBuilder(ABC):

    def __init__(self, meta: ResponseMeta | None):
        if meta is None:
            self.meta = ResponseMeta(timestamp=datetime.now(tz=timezone.utc))
        else:
            self.meta = meta

    @abstractmethod
    def build(self):
        pass
    
    @abstractmethod
    def _build_response(self):
        pass
        
    @abstractmethod
    def _build_payload(self):
        pass


class ApiSuccessResponseBuilder(ApiResponseBuilder, Generic[T]):

    def __init__(
            self, 
            data: T, 
            status: HTTPStatus = HTTPStatus.OK,
            meta: ResponseMeta | None = None,
    ):
        self.data = data
        self.status = status
        super().__init__(meta=meta)

    def build(self) -> ApiSuccessResponse[T]:
        payload = self._build_payload(data=self.data)
        return self._build_response(payload)

    def _build_payload(self, data: T) -> SuccessPayload[T]:
        payload_builder = SuccessPayloadBuilder(data=data)
        return payload_builder.build_payload()    

    def _build_response(self, payload: SuccessPayload[T]) -> ApiSuccessResponse[T]:
        try:
            api_response = ApiSuccessResponse(
                payload=payload,
                status=self.status,
                meta=self.meta,
            ) 
        except Exception as e:
            msg = f"Failed to build ApiSuccessResponse object due to an unexpected error: {e.__class__.__name__}"
            logger.error(msg, exc_info=True)
            raise ApiResponseBuilderError(msg) from e
        else:
            logger.debug(f"Succesfully created ApiSuccessResponse object with status `{self.status}`")
            return api_response


class ApiErrorResponseBuilder(ApiResponseBuilder):
    
    def __init__(
            self,
            error: Exception,
            status: HTTPStatus,
            meta: ResponseMeta | None = None,
    ):
        self.error = error
        self.status = status
        super().__init__(meta=meta)

    def build(self) -> ApiErrorResponse:
        payload = self._build_payload()
        return self._build_response(payload)

    def _build_payload(self) -> ErrorPayload:
        payload_builder = ErrorPayloadBuilder(error=self.error)
        return payload_builder.build_payload()
    
    def _build_response(self, payload: ErrorPayload) -> ApiErrorResponse:
        try:
            api_response = ApiErrorResponse(
                payload=payload,
                status=self.status,
                meta=self.meta,
            ) 
        except Exception as e:
            msg = f"Failed to build ApiErrorResponse object due to an unexpected error: {e.__class__.__name__}"
            logger.error(msg, exc_info=True)
            raise ApiResponseBuilderError(msg) from e
        else:
            logger.debug(f"Succesfully created ApiErrorResponse object with status `{self.status}`")
            return api_response


class ApiPayloadBuilder(ABC):

    success: bool
    data = None
    _error = None

    @abstractmethod
    def build_payload(self):
        pass

    def _either_check(self):
        if self.data is None and self._error is not None:
            return
        elif self.data is not None and self._error is None:
            return
        else:
            msg = (
                f"ApiPayloadBuilder failed to build API payload. Either {self.__class__.__name__}.data "
                f"OR {self.__class__.__name__}.error must be None"
            )
            logger.error(msg)
            raise ApiPayloadBuilderError(msg)


class SuccessPayloadBuilder(ApiPayloadBuilder, Generic[T]):
    """
    Builds an ApiPayload object from either a success payload or an exception.

    Raises:
        ApiPayloadBuilderError: If both or neither of `data` and `error` are provided,
        or if an unexpected error occurs during response construction.
    """
    
    success = True
    
    def __init__(self, data: T):
        self.data = data
        self._error = None
        self._either_check()

    def build_payload(self) -> SuccessPayload[T]:
        try:
            payload = SuccessPayload(success=True, data=self.data, error=None)
        except Exception as e:
            msg = (
                f"{self.__class__.__name__}.build_payload() failed due to an "
                f"unexpected error: `{e.__class__.__name__}`"
            )
            logger.error(msg, exc_info=True)
            raise ApiPayloadBuilderError(msg) from e

        logger.debug(f"Built SuccesPayload from payload data type `{self.data.__class__.__name__}`")
        return payload




class ErrorPayloadBuilder(ApiPayloadBuilder):

    success = False

    def __init__(self, error: Exception):
        self.data = None
        self._error = error
        self._either_check()
      
    def build_payload(self) -> ErrorPayload:
        try:
            error = self._build_error_payload_data()
            payload = ErrorPayload(success=False, data=None, error=error)
        except Exception as e:
            msg = (
                f"{self.__class__.__name__}.build_payload() failed due to an "
                f"unexpected error: `{e.__class__.__name__}`"
            )
            logger.error(msg, exc_info=True)
            raise ApiPayloadBuilderError(msg) from e

        logger.debug(f"Built ErrorPayload from error type `{self._error.__class__.__name__}`")
        return payload

    def _build_error_payload_data(self) -> ErrorPayloadData:
        error_payload = ErrorPayloadData(
            type=self._error.__class__.__name__,
            msg=str(self._error),
        )
        logger.debug(f"Built ErrorPayloadData from error type `{self._error.__class__.__name__}`")

        return error_payload
    