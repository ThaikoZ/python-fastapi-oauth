import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings

env_path = Path('.') / ".env"
print(env_path)
load_dotenv()

class Settings(BaseSettings):
  
  # Database
  DATABASE_URL: str = os.getenv("DATABASE_URL")
  
  # Hashing 
  SECRET_KEY: str  = os.getenv("SUPER_SECRET_KEY")
  ALGORITHM: str  = os.getenv("ALGORITHM")
  ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def get_settings() -> Settings:
    return Settings()