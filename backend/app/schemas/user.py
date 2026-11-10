from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class Prava(str,Enum):
    admin = 'admin'
    klient = 'klient'

class UserCreate(BaseModel):
    email:Optional[str]
    password:str
    first_name:str
    last_name:Optional[str]
    phone:Optional[int]
    role : Prava = Prava.klient

class UserRegistration(BaseModel):
    email:Optional[str]
    password:str
    first_name:str
    last_name:Optional[str]
    phone:Optional[int]

class UserResponse(BaseModel):
     first_name:str
     last_name:Optional[str]
     email:Optional[str]
     phone:Optional[int]

class UserCartShow(BaseModel):
     first_name:str
     last_name:str
     email:str
     phone:str
     model_config = ConfigDict(from_attributes=True)


class UserReviewShow(BaseModel):
     first_name:str
     last_name:str
     email:str
     phone:str
     model_config = ConfigDict(from_attributes=True)


