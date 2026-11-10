from app.database import Base
from datetime import datetime
from enum import Enum


from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column,relationship
from sqlalchemy import String, Boolean, DateTime,func 



class Prava(str,Enum):
    ADMIN = 'admin'
    KLIENT = 'klient'

class User(Base):
    __tablename__ = 'user'
    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    email:Mapped[str] = mapped_column(String, unique=True, nullable = False)
    password:Mapped[str] = mapped_column(String, nullable = False)
    first_name:Mapped[str] = mapped_column(String, nullable = False)
    last_name:Mapped[str] = mapped_column(String, nullable = True)
    phone:Mapped[str] = mapped_column(String, nullable = True)
    is_active:Mapped[bool] = mapped_column(Boolean,default = True)
    role : Mapped[Prava] = mapped_column(default=Prava.KLIENT)

    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cart: Mapped['Cart'] = relationship(back_populates='user')
    order: Mapped['Order'] = relationship(back_populates='user')
    favorite: Mapped['Favorite'] = relationship(back_populates='user')
    review:Mapped['Review'] = relationship(back_populates='user')
    address:Mapped[list['Address']] = relationship(back_populates='user',cascade="all,delete-orphan")