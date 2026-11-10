from pydantic import BaseModel
from typing import List
from app.schemas.user import *
from app.schemas.product import *

class FavoriteBase(BaseModel):
    product_id: int


class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):
    pass


class FavoriteUserShow(BaseModel):
    product: list[ProductFavoriteShow]
    model_config = ConfigDict(from_attributes=True)