from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from users.schemas import CreateUserRequest

router = APIRouter(
  prefix='/users',
  tags=['Users'],
  responses={404: {"description": "Not found"}}
)

@router.get('/')
async def health_check():
  return {"message": "Hello dwa"} 

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
  pass