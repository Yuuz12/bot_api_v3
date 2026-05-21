from pydantic import BaseModel
from typing import Any


class ResponseBase(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any = None


class ErrorResponse(BaseModel):
    code: int
    message: str
