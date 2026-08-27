from app.database import Base
from datetime import datetime


from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String, DateTime,func ,ForeignKey



class Product(Base):
    __tablename__ = 'products'
    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    name : Mapped[str] = mapped_column(String(255), nullable = False)
    description : Mapped[str] = mapped_column(String(600), nullable = False)
    price: Mapped[float] = mapped_column(default = 0.0, nullable = False)
    stock : Mapped[int] = mapped_column(default = 0, nullable = False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    category: Mapped[list['Category']] = relationship(back_populates='products')
    cartitem: Mapped[list['CartItem']] = relationship(back_populates='product',cascade="all,delete-orphan")
    # orderitem: Mapped['OrderItem'] = relationship(back_populates='product_base')
    favorite: Mapped[list['Favorite']] = relationship(back_populates='product',cascade="all,delete-orphan")
    
