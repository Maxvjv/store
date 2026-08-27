from pydantic import BaseModel
from typing import List
from app.schemas.user import *
from app.schemas.product import *

class FavoriteBase(BaseModel):
    user_id: int
    product_id: int


class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):
    pass

class FavoriteProductShow(BaseModel):
    product: ProductCategorySchema

class FavoriteUserShow(BaseModel):
    user: UserCartShow
    product: list[FavoriteProductShow]
    class Config:
            from_attributes = True