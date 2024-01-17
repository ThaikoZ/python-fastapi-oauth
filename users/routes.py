from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db
from users.schemas import CreateUserRequest, UserResponse
from users.services import create_user_account
from core.security import oauth2_scheme

router = APIRouter(
  prefix='/users',
  tags=['Users'],
  responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

user_router = APIRouter(
  prefix='/users',
  tags=['Users'],
  responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
  dependencies=[Depends(oauth2_scheme)]
)

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
  await create_user_account(db, data)
  payload = {"message": "User account has been succesfully created"}
  return JSONResponse(content=payload)

@user_router.post('/me', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def get_user_detail(request: Request):
  return request.user