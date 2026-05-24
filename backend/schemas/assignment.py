from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AssignmentBase(BaseModel):
    item_id: int
    employee_id: int
    notes: Optional[str] = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(BaseModel):
    returned_at: Optional[datetime] = None
    notes: Optional[str] = None


class AssignmentResponse(AssignmentBase):
    id: int

    assigned_at: datetime
    returned_at: Optional[datetime]

    class Config:
        from_attributes = True