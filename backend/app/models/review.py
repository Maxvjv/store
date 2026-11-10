from app.database import Base
from datetime import datetime


from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer, Text, DateTime,func ,ForeignKey
from typing import Optional
from app.models.user import User
from app.models.product import Product


class Review(Base):
    __tablename__ = 'review'
    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'),nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'),nullable=False)
    rating:Mapped[int] = mapped_column(Integer, nullable=False, check_constraint="rating BETWEEN 1 AND 5")
    comment:Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user:Mapped['User'] = relationship(back_populates='review')
    product:Mapped['Product'] = relationship(back_populates='review')