import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings

env_path = Path('.') / ".env"

load_dotenv()

class Settings(BaseSettings):
  
  # Database
  DATABASE_URL: str = os.getenv("DATABASE_URL")
  
  # Jwt Tokens 
  JWT_SECRET: str  = os.getenv("JWT_SECRET")
  JWT_ALGORITHM: str  = os.getenv("JWT_ALGORITHM", "HS256")
  ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_TOKEN_EXPIRE_MINUTES", '30'))


def get_settings() -> Settings:
    return Settings()