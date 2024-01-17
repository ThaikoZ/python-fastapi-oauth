from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db
from users.schemas import CreateUserRequest
from users.services import create_user_account

router = APIRouter(
  prefix='/users',
  tags=['Users'],
  responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

@router.get('/')
async def health_check():
  return {"message": "Hello dwa"} 

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
  await create_user_account(db, data)
  payload = {"message": "User account has been succesfully created"}
  return JSONResponse(content=payload)