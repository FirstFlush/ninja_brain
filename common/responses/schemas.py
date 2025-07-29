from pydantic import BaseModel
from typing import Optional, TypeVar, Generic


T = TypeVar("T")


class ApiErrorResponse(BaseModel):
    type: str
    msg: str


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ApiErrorResponse] = None
    