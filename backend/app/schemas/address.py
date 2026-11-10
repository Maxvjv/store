from pydantic import BaseModel
from typing import Optional


class AddressCreate(BaseModel):
    country : str
    city : str
    street : str
    house : str
    apartment: str
    postal_code : str

class AddressResponse(AddressCreate):
    pass

class AddressOrderShow(BaseModel):
    id:int
    country : str
    city : str
    street : str
    house : str
    apartment: str
    postal_code : str
    class Config:
            from_attributes = True

class AddressUpdate(BaseModel):
    country : Optional[str]
    city : Optional[str]
    street : Optional[str]
    house : Optional[str]
    apartment: Optional[str]
    postal_code : Optional[str]
    
       