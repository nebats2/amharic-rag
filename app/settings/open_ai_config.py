from typing import Optional

from pydantic import BaseModel

from app.commons.json_reader_and_writer import json_reader, json_writer
from app.config_path import OPENAI_CONFIG_FILE_PATH


class OpenAIConfigModel(BaseModel):
    api_key:Optional[str]
    model:str ="gpt-4o"


def get_openai_config_model() -> OpenAIConfigModel:
    try:
        config_file = json_reader(OPENAI_CONFIG_FILE_PATH)
        confi_model: OpenAIConfigModel = OpenAIConfigModel(**config_file)
        return confi_model
    except Exception as ex:
        raise ex


def set_openai_config_model(conf_model: OpenAIConfigModel) -> OpenAIConfigModel:
    try:
        print(f"setting openai config started ..")
        json_writer(OPENAI_CONFIG_FILE_PATH, conf_model)
        confi_model = OpenAIConfigModel(**json_reader(OPENAI_CONFIG_FILE_PATH))
        return confi_model
    except Exception as ex:
        print(f"setting openai config aborted , ex : {ex}")
        raise ex
