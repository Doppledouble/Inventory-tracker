from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.enums import TransactionType


# ─── Nested schemas for response ───────────────────────────
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


# ─── Response ──────────────────────────────────────────────
class StockTransactionResponse(BaseModel):
    id: int
    item: ItemBasic
    employee: Optional[EmployeeBasic] = None
    location: Optional[str] = None
    transaction_type: TransactionType
    quantity: int
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
        
        
        
class StockWithdrawRequest(BaseModel):
    quantity: int
    employee_id: Optional[int] = None
    location: Optional[str] = None
    notes: Optional[str] = None