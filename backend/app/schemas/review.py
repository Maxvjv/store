from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Optional
from app.schemas.user import *
from app.schemas.product import *


class ReviewBase(BaseModel):
    product_id: int
    rating:int
    comment: Optional[str]

class ReviewCreate(BaseModel):
    rating:int
    comment: Optional[str]

class ReviewUpdate(BaseModel):
    product_id: int
    rating:int
    comment: Optional[str]

class ReviewResponse(ReviewBase):
    pass


class ReviewUserShow(BaseModel):
    user:UserReviewShow
    rating:int
    comment: str
    model_config = ConfigDict(from_attributes=True)

class ReviewProductShow(BaseModel):
    product:ProductReviewShow
    reviews:list[ReviewUserShow]
    model_config = ConfigDict(from_attributes=True)
    

