from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Optional
from decimal import Decimal


class ProductBase(BaseModel):
    name: str
    price: float 
    description: str | None = None
    stock: int 
    category_id:int

class ProductDetail(BaseModel):
    id:int
    name:str
    description: str
    price: Decimal
    stock : int
    average_rating: Decimal

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
    id:int
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

class ProductFavoriteShow(BaseModel):
    id:int
    name:str
    price:float
    description: str | None = None
    stock : int
    model_config = ConfigDict(from_attributes=True)

class ProductReviewShow(BaseModel):
    name: str
    price: float 
    description: str | None = None
    average_rating : Decimal
    model_config = ConfigDict(from_attributes=True)

class ProductOrderItems(BaseModel):
    name:str
    description:str
    price:float
    class Config:
            from_attributes = True



     
    


