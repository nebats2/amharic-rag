import shutil
import zipfile
from pathlib import Path
from typing import Any

from fastapi import HTTPException, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, Filter, FieldCondition, MatchValue, \
    PayloadSchemaType

from langchain_core.documents import Document
from qdrant_client.http.exceptions import UnexpectedResponse
from langchain_ollama import OllamaEmbeddings

from app.services.language_service import split_text_by_lang
from app.settings.settings import Setting

setting = Setting()
UPLOADS_DIR = Path("/app/data/uploads")

embedding = OllamaEmbeddings(model=setting.OLLAMA_MODEL, base_url=setting.OLLAMA_URL)
qdrant_client = QdrantClient(
            path= setting.QDRANT_URL,
            prefer_grpc=False
)

def uploaded_file_list():
    return {"files": [str(f.relative_to(UPLOADS_DIR)) for f in UPLOADS_DIR.rglob("*")]}

async def upload_docs(file: UploadFile = File(...)):

    UPLOADS_DIR .mkdir(parents=True, exist_ok=True)

    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed")

    temp_zip_path = UPLOADS_DIR  / file.filename
    with open(temp_zip_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    try:
        with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
            zip_ref.extractall(UPLOADS_DIR )
    except zipfile.BadZipFile:
        temp_zip_path.unlink()  # remove invalid zip
        raise HTTPException(status_code=400, detail="Invalid zip file")

    temp_zip_path.unlink()

    print(f"Uploading completed. Embedding started ..")
    process_dir()
    return  "successfully uploaded"

def process_dir():
    base_dir = Path(UPLOADS_DIR)
    print(f"Processing file directory: {base_dir}")

    if not base_dir.exists() or not base_dir.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")

    results = []

    pdf_files = list(base_dir.rglob("*.pdf"))
    if not pdf_files:
        return "No PDF files found in the directory"

    for file_path in pdf_files:
        if file_path.is_file():
            file_doc = pdf_loader(str(file_path))
            if not file_doc:
                results.append(f"File document for {file_path} not found")
            else:
                vectorize_and_store(file_doc, "document")
                results.append(f"File embedding and storing to qdrant store  for doc path: {file_path} completed successfully")

    return "\n".join(results)

def pdf_loader(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()


def get_qdrant_vector_store():
    setup_collection_store()
    return QdrantVectorStore(
        client=qdrant_client,
        collection_name=setting.QDRANT_COLLECTION,
        embedding=embedding,
        retrieval_mode=RetrievalMode.DENSE
    )

def setup_collection_store():
    print(f"Setting up vector store collection: {setting.QDRANT_COLLECTION}")
    try:
        collections = qdrant_client.get_collections()
        collection_names = [c.name for c in collections.collections]
        print(f"Available collections in Qdrant: {collection_names}")

        if setting.QDRANT_COLLECTION not in collection_names:
            print("Collection not found, creating...")
            qdrant_client.recreate_collection(
                collection_name=setting.QDRANT_COLLECTION,
                vectors_config=VectorParams(
                    size=setting.DIMENSION,
                    distance=Distance.COSINE
                )
            )
            create_indexes()
            print("Collection created and indexes set.")
        else:
            print("Collection already exists, skipping creation.")

    except Exception as ex:
        print(f"Exception while setting up collection: {ex}")
        raise

def vectorize_and_store(docs: list[Document], doc_type:str)->Any:
    try:
        qdrant_vector_store = get_qdrant_vector_store()
        amharic_doc, eng_doc = split_text_by_lang(docs)
        english_chunk = text_splitter(eng_doc, doc_type)

        if amharic_doc is not None and len(amharic_doc) > 0:
            amharic_chunk = text_splitter(amharic_doc, doc_type)
            qdrant_vector_store.add_documents(amharic_chunk)
            print(f"Amharic total chunks stored {len(amharic_chunk)}")
        if eng_doc is not None and len(eng_doc) >0 :
            english_chunk = text_splitter(english_chunk, doc_type)
            qdrant_vector_store.add_documents(english_chunk)
            print(f"English total chunks stored {len(english_chunk)}")

        print(f"embedding and saving to qdrant completed..")
        return "Done"

    except UnexpectedResponse as e:
        print(f"x Qdrant returned an error: {e}")
        raise e

    except Exception as ex:
        print(f"Exception at doc embedding, error : {ex}")
        raise ex

def vectorize_and_store_qa(user_question:str, chat_response:str):
    metadata = {
        "type": "qa",
        "description": user_question
    }
    docs = []
    qa_doc = Document(
        page_content=chat_response + user_question,
        metadata=metadata
    )
    docs.append(qa_doc)
    amharic_doc, eng_doc = split_text_by_lang(docs)
    english_chunk = text_splitter(eng_doc, "qa")

    qdrant_vector_store = get_qdrant_vector_store()
    if amharic_doc is not None and len(amharic_doc) > 0:
        amharic_chunk = text_splitter(amharic_doc, "qa")
        qdrant_vector_store.add_documents(amharic_chunk)
    if eng_doc is not None and len(eng_doc) > 0:
        english_chunk = text_splitter(english_chunk, "qa")
        qdrant_vector_store.add_documents(english_chunk)


def similarity_search_document(prompt : str):
    qdrant_vector_store = get_qdrant_vector_store()
    similar_docs = qdrant_vector_store.similarity_search(query=prompt)
    if similar_docs:
        print(f"Similar docs found size ={len(similar_docs)}")
    else:
        print(f" No document has been found")

    return similar_docs


def create_indexes():

    qdrant_client.create_payload_index(
        collection_name= setting.QDRANT_COLLECTION,
        field_name="language",
        field_schema=PayloadSchemaType.TEXT
    )
    qdrant_client.create_payload_index(
        collection_name=setting.QDRANT_COLLECTION,
        field_name="type",
        field_schema=PayloadSchemaType.TEXT
    )
    print(f"Collection language created")

def text_splitter(docs : list[Document], doc_type:str)-> list[Document]:

        splitter = RecursiveCharacterTextSplitter(chunk_size=setting.DEFAULT_CHUNK_SIZE,
                                                  chunk_overlap=setting.MIN_CHUNK_SIZE_CHARS)

        chunks = splitter.split_documents(docs)

        for chunk in chunks:
            new_metadata = dict(chunk.metadata) if chunk.metadata else {}
            new_metadata["type"] = doc_type
            chunk.metadata = new_metadata

        return chunks