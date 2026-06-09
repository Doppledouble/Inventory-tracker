from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ItemBase(BaseModel):
    name        : str
    category    : Optional[str]
    count       : int = Field(default=0, gt=0)
    

class ItemCreate(ItemBase):
    pass
    
    
class ItemUpdate(BaseModel):
    name        : Optional[str] = None
    category    : Optional[str] = None
    count       : Optional[int] = Field(default=0, gt=0)
    
    
class ItemResponse(ItemBase):
    id          : int
    created_at  : datetime
    updated_at  : Optional[datetime]

    class Config:
        from_attributes = True
    
    
