from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False) 
    location_name = Column(String, nullable=False)   # e.g. "Head Office"
    # code = Column(String, unique=True)      # e.g. "JKT-HO"
    description = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    #relations
    items = relationship("Item", back_populates="location")
    