from fastapi import APIRouter, UploadFile, File, Depends

from app.commons.BaseResponseEntity import BaseResponseEntity
from app.security.auth import verify_token
from app.services.doc_processing import upload_docs, uploaded_file_list, process_dir

router = APIRouter(
    tags=["upload"],
    prefix="/upload"
)

@router.post("/upload")
async def upload_zip(file: UploadFile = File(...), payload: dict = Depends(verify_token)):
    result = await  upload_docs(file)
    response = BaseResponseEntity(
        message="success",
        status= 200,
        body = result
    )
    return response

@router.post("/list")
def list_uploaded(payload: dict = Depends(verify_token)):
    result = uploaded_file_list()
    response = BaseResponseEntity(
        message="success",
        status= 200,
        body = result
    )
    return response

