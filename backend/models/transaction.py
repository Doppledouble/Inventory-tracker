from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from models.enums import TransactionType
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id                  = Column(Integer, primary_key=True)

    item_id             = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity            = Column(Integer, nullable=False)
    transaction_type    = Column(Enum(TransactionType), nullable=False)
    employee_id         = Column(Integer, ForeignKey("employees.id"), nullable=True)
    notes               = Column(String)

    created_at          = Column(DateTime(timezone=True), server_default=func.now())
    item                = relationship("Item", back_populates="transactions")
    employee            = relationship("Employee", back_populates="transactions")