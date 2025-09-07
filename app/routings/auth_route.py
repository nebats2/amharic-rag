from fastapi.routing import APIRoute, APIRouter

from app.commons.BaseResponseEntity import BaseResponseEntity
from app.security.auth import handle_login
from app.security.models import UserLoginRequest

route = APIRouter(
    prefix = "/auth",
    tags=["auth"]
)

@route.post("/login")
def login(login_request: UserLoginRequest)->BaseResponseEntity:
    result = handle_login(login_request)
    return BaseResponseEntity(
        message="success",
        body=result,
        status=200
    )

## more methods to reset password, add user and so on...