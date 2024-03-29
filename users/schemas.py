from pydantic import BaseModel, EmailStr
from typing import Union
from datetime import datetime 
 
class CreateUserRequest(BaseModel):
  first_name: str
  last_name: str
  email: EmailStr
  password: str
  
class BaseResponse(BaseModel):
  class Config:
    from_attributes = True
    arbitrary_types_allowe = True
    
class UserResponse(BaseModel):
  id: int
  first_name: str
  last_name: str
  email: EmailStr
  registered_at: Union[None, datetime] = None
  