from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email:Optional[str]
    password:str
    first_name:str
    last_name:Optional[str]
    phone:Optional[int]
    is_active: bool

class UserResponse(BaseModel):
     first_name:str
     last_name:Optional[str]
     email:Optional[str]
     phone:Optional[int]

class UserCartShow(BaseModel):
     first_name:str
     last_name:str
     email:str
     phone:int
     class Config:
        from_attributes = True

