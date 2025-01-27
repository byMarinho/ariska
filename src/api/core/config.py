import os

from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASS = os.getenv("REDIS_PASS")
REDIS_USER = os.getenv("REDIS_USER", "default")
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_URL = f"redis://{REDIS_USER}:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"


API_ENV = os.getenv("API_ENV", "development")
ARISKA_API_DEV = os.getenv("ARISKA_API_DEV", "http://fastapi:8000")
ARISKA_API_PRD = os.getenv("ARISKA_API_PRD", "http://fastapi:8000")

ARISKA_API = ARISKA_API_DEV if API_ENV == "development" else ARISKA_API_PRD

API_RUN = os.getenv("API_RUN", "local")
DOWNLOAD_SERVER = os.getenv("DOWNLOAD_PATH", "/tmp")
DOWNLOAD_LOCAL = os.getenv("DOWNLOAD_LOCAL", "/tmp")
DOWNLOAD_PATH = DOWNLOAD_LOCAL if API_RUN == "local" else DOWNLOAD_SERVER

PO_TOKEN = os.getenv("PO_TOKEN", "WEB")

os.makedirs(DOWNLOAD_PATH, exist_ok=True)
