from fastapi import APIRouter, status, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from core.database import get_db
from sqlalchemy.orm import Session
from auth.services import get_token, get_refresh_token

router = APIRouter(
  prefix='/auth',
  tags=['Auth'],
  responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

@router.post('/token', status_code=status.HTTP_200_OK)
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  return await get_token(db, data)

@router.post('/refresh', status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
  return await get_refresh_token(db, refresh_token)