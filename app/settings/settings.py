from pathlib import Path

from pydantic_settings import BaseSettings


class Setting (BaseSettings):
    ENV : str = "dev"
    ROOT_USERNAME : str = "admin"
    ROOT_PASSWORD : str
    ROOT_PASSWORD_RAW : str = "123456"
    OLLAMA_MODEL:str
    OLLAMA_URL:str

    QDRANT_URL:str
    QDRANT_API_KEY:str
    QDRANT_COLLECTION:str

    DIMENSION:int=1024

    DEFAULT_CHUNK_SIZE:int = 250
    MIN_CHUNK_SIZE_CHARS : int = 100
    MIN_CHUNK_LENGTH_TO_EMBED : int = 50
    MAX_NUM_CHUNKS : int =  100
    KEEP_SEPARATOR :bool =  True

    class Config:
        env_file = Path(__file__).parent / ".env"
        env_file_encoding = "utf-8"
