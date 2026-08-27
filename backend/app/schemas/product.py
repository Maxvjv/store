from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    name: str
    price: float 
    description: str | None = None
    stock: int 
    category_id:int

class ProductCreate(ProductBase):
    pass  

class ProductResponse(ProductBase):
    id: int
    created_at: datetime

class ProductUpdate(ProductBase):
    name: Optional[str]
    price: Optional[float] 
    description: Optional[str]
    stock: Optional[int] 

class ProductCategorySchema(BaseModel):
    name: str
    price: float 
    description: str | None = None
    stock: int 
    class Config:
        from_attributes = True

class ProductCartShow(BaseModel):
    name:str
    price:float
    description: str | None = None


