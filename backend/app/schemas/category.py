from pydantic import BaseModel
from typing import Optional,List
from app.schemas.product import *

class CategoryBase(BaseModel):
    name: str
    description: Optional[str]
    parent_id: Optional[int] 


class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    name: str
    description: str
    

class CategoryUpdate(CategoryBase):
    name: Optional[str]
    description: Optional[str]
    parent_id: Optional[int]

class CategoryWithProduct(BaseModel):
    id:int
    name: str
    description:str
    products: List[ProductCategorySchema]
    class Config:
        from_attributes = True


