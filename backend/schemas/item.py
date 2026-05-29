from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from models.enums import ItemStatus

class ItemBase(BaseModel):
    name        : str
    category    : Optional[str]
    count       : int = Field(default=0, gt=0)
    

class ItemCreate(ItemBase):
    location_id : Optional[int] = None
    
    
class ItemUpdate(BaseModel):
    name        : Optional[str] = None
    category    : Optional[str] = None
    count       : Optional[int] = Field(default=0, gt=0)
    location_id : Optional[int] = None
    # status      : Optional[ItemStatus] = None
    
    
class ItemResponse(ItemBase):
    id          : int
    status      : Optional[ItemStatus]
    location_id : Optional[int]
    created_at  : datetime
    updated_at  : Optional[datetime]

    class Config:
        from_attributes = True
    
    
