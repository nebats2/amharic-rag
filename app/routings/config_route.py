from fastapi import APIRouter, Depends

from app.commons.BaseResponseEntity import BaseResponseEntity
from app.security.auth import verify_token
from app.settings.open_ai_config import get_openai_config_model, OpenAIConfigModel, set_openai_config_model

router = APIRouter(
    prefix = "/config",
    tags=["config"]
)

@router.get("/openai")
def openai_config(payload: dict = Depends(verify_token))->BaseResponseEntity:
    result = get_openai_config_model()
    response = BaseResponseEntity(
        message="success",
        status=200,
        body=result
    )
    return response

@router.post("/openai")
def openai_config_set(model: OpenAIConfigModel, payload: dict = Depends(verify_token))->BaseResponseEntity:
    result = set_openai_config_model(model)
    response = BaseResponseEntity(
        message="success",
        status=200,
        body=result
    )
    return response