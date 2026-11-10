from pydantic import BaseModel
from typing import List
from app.schemas.user import *
from app.schemas.category import *


class CartBase(BaseModel):
    user_id : int

class CartCreate(CartBase):
    pass

class CartResponse(BaseModel):
    cart_id:int
    product_id : int
    quantity:int

class CartItemBase(BaseModel):
    product_id : int


class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(CartItemBase):
    quantity:int

class CartItemProd(BaseModel):
     product : ProductCartShow
     quantity:int

class CartShowWithUser(BaseModel):
    user: UserCartShow
    cartitem : list[CartItemProd]
    class Config:
            from_attributes = True