from app.database import Base
from datetime import datetime
from enum import Enum
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text, DateTime, Integer,func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Status(str,Enum):
    PENDING = 'pending'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    REFUNDED = 'refunded'

class Payment(Base):
    __tablename__ = 'payment'
    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"),nullable=False)
    amount : Mapped[Decimal] = mapped_column(Numeric(10, 2),default=Decimal('0.00'))
    status: Mapped[Status] = mapped_column(default=Status.PENDING)
    payment_method :Mapped[str] = mapped_column(String,default='cart',nullable=False)
    transaction_id :Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())



    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())