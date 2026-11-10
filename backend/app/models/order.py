from app.database import Base
from datetime import datetime
from enum import Enum
from decimal import Decimal



from sqlalchemy import ForeignKey, Numeric, String, Text, DateTime, Integer,func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.user import User
from app.models.product import Product

class Status(str,Enum):
    PENDING = 'pending'
    PAID = 'paid'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    

class Order(Base):
    __tablename__ = 'order'
    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"),nullable= False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[Status] = mapped_column(default=Status.PENDING)
    total_amount : Mapped[Decimal] = mapped_column(Numeric(10, 2),default=Decimal('0.00'))
    shipping_address: Mapped[int] = mapped_column(Integer, nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(20),nullable=False)


    user: Mapped['User'] = relationship(back_populates='order')
    orderitem : Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = 'orderitem'
    id: Mapped[int] = mapped_column(primary_key= True, index= True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'),nullable= False)
    product_id:Mapped[int] = mapped_column(ForeignKey('products.id'),nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_time:Mapped[Decimal] = mapped_column(Numeric(10, 2))


    product: Mapped[Product] = relationship(back_populates='orderitem')
    order: Mapped['Order'] = relationship(back_populates='orderitem')