from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EmployeeBase(BaseModel):
    first_name  : str
    last_name : str
    email       : str
    is_admin    : bool
    
class EmployeeCreate(EmployeeBase):
    pass
    
    
class EmployeeUpdate(BaseModel):
    first_name  : Optional[str] = None
    last_name : Optional[str] = None
    email       : Optional[str] = None
    is_admin    : Optional[bool]= None


class LocationResponse(EmployeeBase):
    id          : int
    created_at  : datetime
    updated_at  : Optional[datetime]
    
    class config:
        from_attributes = True