from pydantic import BaseModel
from typing import List
from decimal import Decimal
from enum import Enum
from datetime import datetime

from app.schemas.product import ProductOrderItems
from app.schemas.address import AddressOrderShow

class OrderStatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderItems(BaseModel):
    order_id:int
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    shipping_address:int
    contact_phone:str

class OrderResponse(BaseModel):
    user_id : int
    created_at : datetime
    status: OrderStatusEnum
    total_amount: Decimal
    shipping_address: int
    contact_phone: str

class OrderListShow(BaseModel):
    id:int
    created_at : datetime
    status: OrderStatusEnum
    total_amount: Decimal
    shipping_address:int
    contact_phone: str

class OrderItemsShow(BaseModel):
    order_id:int
    product:ProductOrderItems
    quantity:int
    price_at_time:Decimal
    
