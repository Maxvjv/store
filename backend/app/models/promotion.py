from app.database import Base
from datetime import datetime
from decimal import Decimal
from enum import Enum


from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Text, Boolean, DateTime,DECIMAL,ForeignKey,Table

from app.models.product import Product
from app.models.category import Category

class Type(str,Enum):
   PERCENTAGE = 'percentage'
   FIXED = 'fixed'

class Who(str,Enum):
    ALL = 'all'
    PRODUCT = 'product'
    CATEGORY = 'category'


class PromotionProducts(Base):
    __tablename__ = "promotion_products"
    id : Mapped[int] = mapped_column(primary_key = True, index = True, autoincrement=True)
    promotion_id: Mapped[int] = mapped_column("promotion_id", ForeignKey("promotion.id"), nullable=False)
    product_id : Mapped[int] = mapped_column("product_id", ForeignKey("products.id"), nullable=False)
    promotions: Mapped[list["Promotion"]] = relationship(back_populates="products")
    products: Mapped[list['Product']] = relationship(back_populates='promotions')

class PromotionCategories(Base):
    __tablename__ = "promotion_categories"
    id : Mapped[int] = mapped_column(primary_key = True, index = True, autoincrement=True)
    promotion_id: Mapped[int] = mapped_column("promotion_id", ForeignKey("promotion.id"), nullable=False)
    category_id : Mapped[int]= mapped_column("category_id", ForeignKey("category.id"), nullable=False) 
    promotions: Mapped[list["Promotion"]] = relationship(back_populates="categories")
    categories : Mapped[list["Category"]] = relationship(back_populates="promotions")

class Promotion(Base):
    __tablename__ = 'promotion'
    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    name : Mapped[str] = mapped_column(String(255), nullable = False)
    description:Mapped[str] = mapped_column(Text, nullable=True)
    discount_type: Mapped[Type] = mapped_column(default=Type.PERCENTAGE)
    discount_value: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active:Mapped[bool] = mapped_column(Boolean,default = True)
    applicable_to: Mapped[Who] = mapped_column(default=Who.PRODUCT)


    # Связи many-to-many
    products: Mapped[list["PromotionProducts"]] = relationship(back_populates="promotions")
    categories: Mapped[list["PromotionCategories"]] = relationship(back_populates="promotions")