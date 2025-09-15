import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://requests_user:1234@127.0.0.1:5432/requests_db")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALG = os.getenv("JWT_ALG")
ACCESS_TOKEN_MIN = int(os.getenv("ACCESS_TOKEN_MIN"))
