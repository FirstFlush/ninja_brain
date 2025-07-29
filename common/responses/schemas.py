from http import HTTPStatus
from pydantic import BaseModel
from typing import Optional, TypeVar, Generic


T = TypeVar("T")


class ApiErrorPayload(BaseModel):
    type: str
    msg: str

class ApiPayload(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ApiErrorPayload] = None

class ApiResponse(BaseModel, Generic[T]):
    payload: ApiPayload[T]
    status: HTTPStatus