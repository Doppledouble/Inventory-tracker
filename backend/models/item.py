from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base
from models.enums import ItemStatus


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, nullable=False)
    category = Column(String)
    count = Column(Integer, nullable=False)
    status = Column(Enum(ItemStatus), default=ItemStatus.AVAILABLE, nullable=False)
    # serial_number = Column(String, unique=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    #relation columns
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    # employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    #relations
    location = relationship("Location", back_populates="items")
    assignments = relationship("Assignmnet", back_populates="item", cascade="all, delete-orphan")
    # employee = relationship("Employee", back_populates="items")