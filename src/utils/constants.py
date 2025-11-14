import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

# Project Constants
DATA_DIR = Path(os.getenv("DATA_DIR")) 
GEE_PROJECT_NAME = os.getenv("GEE_PROJECT_NAME")
