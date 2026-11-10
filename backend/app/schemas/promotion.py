from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from enum import Enum

class Type(str,Enum):
   percentage = 'percentage'
   fixed = 'fixed'

class Who(str,Enum):
    all = 'all'
    product = 'product'
    category = 'category'

class PromotionCreate(BaseModel):
    name : str
    description: str
    discount_type: Type
    discount_value: Decimal
    start_date: datetime
    end_date: datetime
    is_active:bool
    applicable_to: Who

class PromoProductCreate(BaseModel):
    promotion_id: int
    product_id : int 

class PromoCategoryCreate(BaseModel):
    promotion_id: int
    category_id : int


