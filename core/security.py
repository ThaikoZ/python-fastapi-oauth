from fastapi import Header, Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from datetime import timedelta, datetime
from jose import jwt, JWTError
from core.config import get_settings
from core.database import get_db
from users.models import UserModel

settings = get_settings()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

def get_password_hash(password: str):
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
  return pwd_context.verify(plain_password, hashed_password)

async def create_access_token(data: dict, expiry: timedelta):
  payload = data.copy()
  expire_in = datetime.utcnow() + expiry
  payload.update({"exp": expire_in})
  return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def create_refresh_token(data: dict):
  return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def get_token_payload(token: str =  Header()):
  try:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
  except JWTError:
    return None
  return payload

def get_current_user(token: str = Depends(oauth2_scheme), db = None):
  payload = get_token_payload(token)
  if not payload or type(payload) is not dict:
    return None
  
  user_id = payload.get('id', None)
  if not user_id:
    return None
  
  if not db:
    db = next(get_db())
    
  user = db.query(UserModel).filter(UserModel.id == user_id).first()
  return user


class JWTAuth:
  async def authenticate(self, conn):
    guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()
    
    if 'authorization' not in conn.headers:
      return guest
    
    token = conn.headers.get('authorization').split(' ')[1]
    if not token:
      return guest
    
    user = get_current_user(token)
    if not user:
      return guest
    
    return AuthCredentials('authenticated'), user