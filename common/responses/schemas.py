from datetime import datetime
from http import HTTPStatus
from pydantic import BaseModel, field_validator
from typing import Any, Literal, TypeVar, Optional, Generic


T = TypeVar("T")


class SuccessPayload(BaseModel, Generic[T]):
    success: Literal[True]
    data: T
    error: None

class ErrorPayloadData(BaseModel):
    type: str
    msg: str

class ErrorPayload(BaseModel):
    success: Literal[False]
    data: None
    error: ErrorPayloadData

class ResponseMeta(BaseModel):
    duration: Optional[float] = None
    extra: Optional[dict[str, Any]] = None
    method: Optional[str] = None
    path: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    version: Optional[str] = None

    @field_validator("method")
    @classmethod
    def normalize_method(cls, v):
        if isinstance(v, str):
            return v.upper()
        return v

class ApiResponse(BaseModel):
    status: HTTPStatus
    meta: Optional[ResponseMeta] = None
    
    
class ApiSuccessResponse(ApiResponse, Generic[T]):
    payload: SuccessPayload[T]

class ApiErrorResponse(ApiResponse):
    payload: ErrorPayload
