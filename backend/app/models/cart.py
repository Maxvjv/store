from app.database import Base
from datetime import datetime


from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String, Text, DateTime,func ,ForeignKey
from typing import Optional

from app.models.user import User
from app.models.product import Product


class Cart(Base):
    __tablename__ = 'cart'
    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"),unique=True,nullable= False)

    user: Mapped["User"] = relationship(back_populates="cart")
    cartitem : Mapped[list['CartItem']] = relationship(back_populates='cart')

class CartItem(Base):
    __tablename__ = 'cartitem'
    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    cart_id : Mapped[int] = mapped_column(ForeignKey("cart.id"),nullable= False)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"),nullable= False)
    quantity: Mapped[int] = mapped_column(default = 1, nullable = False)
    added_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cart: Mapped[list['Cart']] = relationship(back_populates='cartitem')
    product: Mapped[list['Product']] = relationship(back_populates='cartitem')
