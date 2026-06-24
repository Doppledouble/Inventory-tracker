from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from models.enums import ItemType

class ItemBase(BaseModel):
    name        : str
    category    : Optional[str]
    type        : ItemType
    count       : int = Field(default=0, gt=0)
    unit        : str
    

class ItemCreate(ItemBase):
    pass
    
    
class ItemUpdate(BaseModel):
    name        : Optional[str] = None
    category    : Optional[str] = None
    type        : Optional[ItemType] = None
    count       : Optional[int] = Field(default=0, ge=0)
    unit        : Optional[str] = None
    
    
class ItemResponse(ItemBase):
    id          : int
    created_at  : datetime
    updated_at  : Optional[datetime]

    class Config:
        from_attributes = True
    
    
