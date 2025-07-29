import logging
from typing import Generic, TypeVar
from .errors import ApiResponseBuilderError
from .schemas import ApiResponse, ApiErrorResponse


logger = logging.getLogger(__name__)
T = TypeVar("T")


class ApiResponseBuilder(Generic[T]):
    """
    Builds an ApiResponse object from either a success payload or an exception.

    This class enforces that exactly one of `data` or `error` is provided,
    and generates a structured response accordingly. Use `from_data()` or
    `from_error()` to create instances, then call `build_response()` to 
    produce the final ApiResponse.

    Raises:
        ApiResponseBuilderError: If both or neither of `data` and `error` are provided,
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

    @classmethod
    def from_data(cls, data: T) -> "ApiResponseBuilder[T]":
        return cls(data=data, error=None)
    
    @classmethod
    def from_error(cls, e: Exception) -> "ApiResponseBuilder[T]":
        return cls(data=None, error=e)

    def build_response(self) -> ApiResponse:
        try:
            error = self._build_error_response()
            api_response = ApiResponse(
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
            raise ApiResponseBuilderError(msg) from e
        else:
            logger.debug(f"Built ApiResponse with payload data type `{self.data.__class__.__name__}`")            
            return api_response

    def _build_error_response(self) -> ApiErrorResponse | None:
        if self._error:
            error_response = ApiErrorResponse(
                type=self._error.__class__.__name__,
                msg=str(self._error),
            )
            logger.debug(f"Built error response for `{self._error.__class__.__name__}`")
        else:
            error_response = None
            
        return error_response
    
    def _either_check(self):
        if self.data is None and self._error is not None:
            return
        elif self.data is not None and self._error is None:
            return
        else:
            msg = (
                f"Failed to build ApiResponse. Either {self.__class__.__name__}.data "
                f"OR {self.__class__.__name__}.error must be None"
            )
            logger.error(msg)
            raise ApiResponseBuilderError(msg)

    def _success(self) -> bool:
        return self.data is not None and self._error is None