
from urllib.request import Request

from fastapi.exceptions import RequestValidationError
from openai import UnprocessableEntityError
from starlette.responses import JSONResponse

from app.routings import chat_route, upload_route, auth_route, config_route

from fastapi import FastAPI

from app.services.doc_processing import setup_collection_store

app = FastAPI(
    title = "Amharic RAG",
    summary = "Simple RAG API detecting and splitting pdf law documents language wise, vectorizing and embedding to local qdrant store and providing context to chat LLM",
    description= """
    Amharic help you 
    # Upload and process ziped PDF law files, writen in Amharic or English scripts
    # Split and vectorize the contents language wise for efficiency and optimal retrieval
    # Retrieve and load based on the user question and build a context for LLM
    # Set OpenAI access api_key and model options to chat
    # You can set the Ollama embedding model, dimensions in the environment setting file
    """)

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





