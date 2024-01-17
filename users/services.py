from users.schemas import CreateUserRequest
from fastapi import status, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from core.security import get_password_hash
from users.models import UserModel

async def create_user_account(db: Session, data: CreateUserRequest):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email is already registered")

    new_user = UserModel(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=get_password_hash(data.password), 
        is_active=False,
        is_verified=False,
        registered_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user