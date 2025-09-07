
from urllib.request import Request

from fastapi.exceptions import RequestValidationError
from openai import UnprocessableEntityError
from starlette.responses import JSONResponse

from app.routings import chat_route, upload_route, auth_route, config_route

from fastapi import FastAPI

from app.services.doc_processing import setup_collection_store

app = FastAPI()
app.include_router(chat_route.router)
app.include_router(upload_route.router)
app.include_router(auth_route.route)
app.include_router(config_route.router)

@app.on_event("startup")
async def startup_event():
    setup_collection_store()

@app.exception_handler(UnprocessableEntityError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors(), "body": exc.body})





