from app.database import Base
from datetime import datetime


from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String, Text, DateTime,func ,ForeignKey
from typing import Optional

from app.models.user import User
from app.models.product import Product

class Favorite(Base):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"),nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'),nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


    user:Mapped['User'] = relationship(back_populates='favorite')
    product:Mapped[list['Product']] = relationship(back_populates='favorite')