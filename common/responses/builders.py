from http import HTTPStatus
import logging
from typing import Generic, TypeVar
from .errors import ApiPayloadBuilderError, ApiResponseBuilderError
from .schemas import ApiPayload, ApiErrorPayload, ApiResponse


logger = logging.getLogger(__name__)
T = TypeVar("T")


class ApiResponseBuilder(Generic[T]):
    
    def __init__(
            self, 
            payload: ApiPayload[T], 
            status: HTTPStatus,
    ):
        self.payload = payload
        self.status = status

    @classmethod
    def from_data(cls, data: T, status: HTTPStatus = HTTPStatus.OK) -> "ApiResponse[T]":
        payload = cls._build_payload(data=data, error=None)
        response_builder = cls(payload=payload, status=status)
        return response_builder._build_response()
    
    @classmethod
    def from_error(cls, e: Exception, status: HTTPStatus) -> "ApiResponse[T]":
        payload = cls._build_payload(data=None, error=e)
        response_builder = cls(payload=payload, status=status)
        return response_builder._build_response()

    @staticmethod
    def _build_payload(data: T | None, error: Exception | None) -> "ApiPayload[T]":
        payload_builder = ApiPayloadBuilder(data=data, error=error)
        return payload_builder.build_payload()    
    
    def _build_response(self) -> ApiResponse:
        try:
            api_response = ApiResponse(
                payload=self.payload,
                status=self.status
            ) 
        except Exception as e:
            msg = f"Failed to build ApiResponse object due to an unexpected error: {e.__class__.__name__}"
            logger.error(msg, exc_info=True)
            raise ApiResponseBuilderError(msg) from e
        else:
            logger.debug(f"Succesfully created ApiResponse object with status `{self.status}`")
            return api_response

class ApiPayloadBuilder(Generic[T]):
    """
    Builds an ApiPayload object from either a success payload or an exception.

    Raises:
        ApiPayloadBuilderError: If both or neither of `data` and `error` are provided,
        or if an unexpected error occurs during response construction.
    """
    def __init__(
            self, 
            data: T | None,
            error: Exception | None,
    ):
        self.data = data
        self._error = error
        self._either_check()
        self.success = self._success()


    def build_payload(self) -> ApiPayload:
        try:
            error = self._build_error_payload()
            api_payload = ApiPayload(
                success=self.success,
                data=self.data,
                error=error,
            )
        except Exception as e:
            msg = (
                f"{self.__class__.__name__}.build_response() failed due to an "
                f"unexpected error: `{e.__class__.__name__}`"
            )
            logger.error(msg, exc_info=True)
            raise ApiPayloadBuilderError(msg) from e
        else:
            logger.debug(f"Built ApiPayload with payload data type `{self.data.__class__.__name__}`")            
            return api_payload

    def _build_error_payload(self) -> ApiErrorPayload | None:
        if self._error:
            error_payload = ApiErrorPayload(
                type=self._error.__class__.__name__,
                msg=str(self._error),
            )
            logger.debug(f"Built ApiErrorPayload for `{self._error.__class__.__name__}`")
        else:
            error_payload = None
            
        return error_payload
    
    def _either_check(self):
        if self.data is None and self._error is not None:
            return
        elif self.data is not None and self._error is None:
            return
        else:
            msg = (
                f"Failed to build ApiPayload. Either {self.__class__.__name__}.data "
                f"OR {self.__class__.__name__}.error must be None"
            )
            logger.error(msg)
            raise ApiPayloadBuilderError(msg)

    def _success(self) -> bool:
        return self.data is not None and self._error is None