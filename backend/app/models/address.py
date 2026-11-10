from app.database import Base
from datetime import datetime


from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String, Boolean, DateTime,func ,ForeignKey

from app.models.user import User


class Address(Base):
    __tablename__ = 'address'
    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"),nullable= False)
    country : Mapped[str] = mapped_column(String, nullable = False)
    city : Mapped[str] = mapped_column(String, nullable = False)
    street : Mapped[str] = mapped_column(String, nullable = False)
    house : Mapped[str] = mapped_column(String, nullable = False)
    apartment:Mapped[str] = mapped_column(String, nullable = False)
    postal_code : Mapped[str] = mapped_column(String, nullable = False)
    is_default:Mapped[bool] = mapped_column(Boolean,default = True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user:Mapped['User'] = relationship(back_populates='address')

