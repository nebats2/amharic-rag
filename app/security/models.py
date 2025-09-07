from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    id:int
    username:str
    hashed_password:str
    roles :Optional[list[str]]


class UserResponseModel(BaseModel):
    id:int
    username:str
    roles: Optional[list[str]]

class UserLoginRequest(BaseModel):
    username:str
    raw_password:str