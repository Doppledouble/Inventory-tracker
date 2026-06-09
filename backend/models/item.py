from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, nullable=False)
    category = Column(String)
    count = Column(Integer, nullable=False)
    # serial_number = Column(String, unique=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    #relations
    assignments = relationship("Assignment", back_populates="item", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="item", cascade="all, delete-orphan")
    # employee = relationship("Employee", back_populates="items")