from typing import overload, TypeVar
from http import HTTPStatus
from .errors import ApiResponseBuilderError
from .schemas import ApiSuccessResponse, ApiErrorResponse, ResponseMeta
from .builders import ApiSuccessResponseBuilder, ApiErrorResponseBuilder, ApiResponseBuilder

T = TypeVar("T")

# Overload for success
@overload
def build_api_response(
    *,
    data: T,
    error: None = None,
    status: HTTPStatus = HTTPStatus.OK,
    meta: ResponseMeta | None = None,
) -> ApiSuccessResponse[T]: ...

# Overload for error
@overload
def build_api_response(
    *,
    data: None = None,
    error: Exception,
    status: HTTPStatus,
    meta: ResponseMeta | None = None,
) -> ApiErrorResponse: ...

def build_api_response(
    *,
    data: T | None = None,
    error: Exception | None = None,
    status: HTTPStatus = HTTPStatus.OK,
    meta: ResponseMeta | None = None,
) -> ApiSuccessResponse[T] | ApiErrorResponse:
    ApiResponseBuilder.assert_one_of(data=data, error=error)
    try:
        if data:
            return ApiSuccessResponseBuilder(data=data, status=status, meta=meta).build()
        if error:
            return ApiErrorResponseBuilder(error=error, status=status, meta=meta).build()
    except Exception as e:
        msg = f"Failed to build API response object due to an unexpected error: `{e.__class__.__name__}`"
        raise ApiResponseBuilderError(msg) from e
    else:
        raise ApiResponseBuilderError(f"Unable to build API response with data type `{data}` and error type `{error}`")