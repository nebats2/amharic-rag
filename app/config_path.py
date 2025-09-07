import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR =   Path(PROJECT_DIR / "data/configs")

OPENAI_CONFIG_FILE_PATH = CONFIG_DIR / "openai_config.json"