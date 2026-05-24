from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LocationBase(BaseModel):
    city            : str
    location_name   : str
    description     : Optional[str] = None
    
    
class LocationCreate(LocationBase):
    pass
    
    
class LocationUpdate(BaseModel):
    city            : Optional[str] = None
    location_name   : Optional[str] = None
    description     : Optional[str] = None


class LocationResponse(LocationBase):
    id          : int
    created_at  : datetime
    updated_at  : Optional[datetime]
    
    class config:
        from_attributes = True