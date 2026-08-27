from app.database import Base
from datetime import datetime


from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String, Text, DateTime,func ,ForeignKey
from typing import Optional

from app.models.product import Product

class Category(Base):
    __tablename__ = 'category'
    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    name :Mapped[str] = mapped_column(String, unique=True, nullable = False)
    description : Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parent_id:Mapped[Optional[int]] = mapped_column(ForeignKey("category.id",ondelete='CASCADE'),nullable=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category",cascade="all,delete-orphan")
