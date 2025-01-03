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
ARISKA_API_DEV = os.getenv("ARISKA_API_DEV", "http://localhost:8000")
ARISKA_API_PRD = os.getenv("ARISKA_API_PRD", "http://localhost:8000")

ARISKA_API = ARISKA_API_DEV if API_ENV == "development" else ARISKA_API_PRD

DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "/tmp")

os.makedirs(DOWNLOAD_PATH, exist_ok=True)
