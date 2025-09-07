from pydantic import BaseModel
from typing import Optional, Any


class BaseResponseEntity(BaseModel) :
    message : str
    requestId : Optional[str] = None
    body : Any
    status: int = 500   # default is an internal server exception
    code : Optional[str] = None
