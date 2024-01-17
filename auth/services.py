from fastapi import APIRouter, status, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from users.models import UserModel
from core.security import verify_password
from core.config import get_settings
from datetime import timedelta
from core.security import create_access_token, create_refresh_token, get_token_payload
from auth.responses import TokenResponse

settings = get_settings()

async def get_token(db: Session, data: OAuth2PasswordRequestForm = Depends()):
  user = db.query(UserModel).filter(UserModel.email == data.username).first()  
  
  if not user:
    raise HTTPException (
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail="Email is not registered", 
      headers={"WWW-Authenticate": "Bearer"}
    )
  
  if not verify_password(data.password, user.hashed_password):
    raise HTTPException (
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail="Invalid Login Credentials", 
      headers={"WWW-Authenticate": "Bearer"}
    )
    
  _verify_user_access(user)
  
  return await _get_user_token(user)
    
    
async def get_refresh_token(db: Session, token: str = Header()):
  payload = get_token_payload(token)
  user_id = payload.get('id', None)
  if not user_id:
    raise HTTPException (
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail="Invalid refresh token", 
      headers={"WWW-Authenticate": "Bearer"}
    )
  user = db.query(UserModel).filter(UserModel.id == user_id).first()
  if not user:
    raise HTTPException (
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail="Invalid refresh token", 
      headers={"WWW-Authenticate": "Bearer"}
    )
    
  return await _get_user_token(user, refresh_token=token)


def _verify_user_access(user: UserModel):
  if not user.is_active:
    raise HTTPException (
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail="Your account is inactive. Please contact support", 
      headers={"WWW-Authenticate": "Bearer"}
    )
  
  if not user.is_verified:
    # Trigger user account verification
    raise HTTPException (
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail="Your account is unverfied. We have resend the account verification email", 
      headers={"WWW-Authenticate": "Bearer"}
    )
    
async def _get_user_token(user: UserModel, refresh_token = None):
  payload = { "id": user.id }
  
  access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  
  access_token = await create_access_token(payload, access_token_expiry)
  if not refresh_token:
    refresh_token = await create_refresh_token(payload)
    
  return TokenResponse(
    access_token=access_token,
    refresh_token=refresh_token,
    expires_in=access_token_expiry.seconds
  )