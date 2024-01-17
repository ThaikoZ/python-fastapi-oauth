import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseSettings

env_path = Path('.') / ".env"
load_dotenv()

SECRET_KEY = os.getenv("SUPER_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

    

