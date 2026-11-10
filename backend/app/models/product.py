from app.database import Base
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Numeric


from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,DateTime,func ,ForeignKey



class Product(Base):
    __tablename__ = 'products'
    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    name : Mapped[str] = mapped_column(String(255), nullable = False)
    description : Mapped[str] = mapped_column(String(600), nullable = False)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), default=Decimal('0.00'),nullable=False)
    stock : Mapped[int] = mapped_column(default = 0, nullable = False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    average_rating: Mapped[Decimal] = mapped_column(Numeric(precision=4, scale=2), default=Decimal('0.00'), nullable=False )

    category: Mapped['Category'] = relationship(back_populates='products')
    cartitem: Mapped[list['CartItem']] = relationship(back_populates='product',cascade="all,delete-orphan")
    orderitem: Mapped['OrderItem'] = relationship(back_populates='product')
    favorite: Mapped['Favorite'] = relationship(back_populates='product',cascade="all,delete-orphan")
    review: Mapped['Review'] = relationship(back_populates='product',cascade="all,delete-orphan")
    promotions: Mapped[list["PromotionProducts"]] = relationship(back_populates="products")
    
