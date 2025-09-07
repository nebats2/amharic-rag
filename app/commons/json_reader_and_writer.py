import json
from typing import Any

# this json file read and write is primary used to save configuration values to the config files

def json_reader(f_path : str) -> Any:
    try:
        with open(f_path, "r") as r:
            file_json = json.load(r)
            return file_json
    except Exception as ex:
        print(f"Exception reading file path :{f_path}, ex :{ex}")
        raise ex

def json_writer(f_path:str, data: Any):
    try:
        with open(f_path, "w") as w:
            w.write(data.model_dump_json(indent=4))
    except Exception as ex:
        print(f"Exception file writing file path :{f_path}, ex : {ex}")
        raise ex