from fastapi import APIRouter, Depends

from app.commons.BaseResponseEntity import BaseResponseEntity
from app.security.auth import verify_token
from app.services.chat_service import chat_document
from app.services.doc_processing import similarity_search_document

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)
@router.post("/")
def chat(prompt : str, payload: dict = Depends(verify_token)) ->BaseResponseEntity:
    result  = chat_document(prompt)
    return BaseResponseEntity(
        message="success",
        body=result,
        status=200
    )

@router.get("/similarity")
def similarity_search(prompt :str, payload: dict = Depends(verify_token))->BaseResponseEntity:
    result = similarity_search_document(prompt)
    return BaseResponseEntity(
        message="success",
        body=result,
        status=200
    )
