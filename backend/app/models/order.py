# from app.database import Base
# from datetime import datetime
# from sqlalchemy import Enum
# from decimal import Decimal
# from enum import Enum as PyEnum


# from sqlalchemy.orm import Mapped,mapped_column,relationship
# from sqlalchemy import String, Integer, Text, Numeric, DateTime,func ,ForeignKey
# from typing import Optional

# from app.models.user import User
# from app.models.product import Product

# class Status(PyEnum):
#     PENDING = 'pending'
#     PAID = 'paid'
#     SHIPPED = 'shipped'
#     DELIVERED = 'delivered'
#     CANCELLED = 'cancelled'

    

# class Order(Base):
#     __tablename__ = 'order'
#     id : Mapped[int] = mapped_column(primary_key = True, index = True)
#     user_id : Mapped[int] = mapped_column(ForeignKey("user.id"),unique=True,nullable= False)
#     created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
#     status: Mapped[Status] = mapped_column(Enum(Status))
#     total_amount : Mapped[Decimal] = mapped_column(Numeric(10, 2))
#     shipping_address: Mapped[str] = mapped_column(Text, nullable=False)
#     contact_phone: Mapped[str] = mapped_column(String,nullable=False)


#     user: Mapped['User'] = relationship(back_populates='order')
#     orderitem : Mapped['OrderItem'] = relationship(back_populates='orderbase')

# class OrderItem(Base):
#     __tablename__ = 'orderitem'
#     id: Mapped[int] = mapped_column(primary_key= True, index= True)
#     order_id: Mapped[int] = mapped_column(ForeignKey('order.id',unique=True,nullable= False))
#     product_id:Mapped[int] = mapped_column(ForeignKey('product.id',nullabe=False))
#     quantity: Mapped[int] = mapped_column(Integer, nullable=False)
#     price_at_time:Mapped[Decimal] = mapped_column(Numeric(10, 2))


#     product_base: Mapped[Product] = relationship(back_populates='orderitem')
#     orderbase: Mapped['Order'] = relationship(back_populates='orderitem')