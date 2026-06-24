from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AssignmentBase(BaseModel):
    item_id: int
    employee_id: int
    location: str
    quantity: int
    notes: str | None = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(BaseModel):
    # returned_at: Optional[datetime] = None
    notes: Optional[str] = None
    
    
class ItemBasic(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True
        
        
class EmployeeBasic(BaseModel):
    id: int
    first_name: str
    last_name: str
    
    class Config:
        from_attributes = True
        

class AssignmentResponse(BaseModel):
    id: int
    quantity: int    
    assigned_at:datetime
    returned_at:datetime | None

    item: ItemBasic       # { id, name }
    employee: EmployeeBasic  # { id, first_name, last_name }
    location: str  

    class Config:
        from_attributes = True