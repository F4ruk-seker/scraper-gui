from pathlib import Path
from models import ApiHostModel


API_HOST = ApiHostModel("http://127.0.0.1:8000/api")
DEBUG = False

BASE_DIR = Path(__file__).resolve().parent

