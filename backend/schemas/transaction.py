from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.enums import TransactionType


# ─── Request ───────────────────────────────────────────────
class StockTransactionRequest(BaseModel):
    quantity: int
    notes: Optional[str] = None
    employee_id: Optional[int] = None  


class StockAdjustmentRequest(BaseModel):
    new_quantity: int  
    notes: Optional[str] = None
    employee_id: Optional[int] = None

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
    item_id: int
    item: ItemBasic                         
    employee_id: Optional[int] = None
    employee: Optional[EmployeeBasic] = None  
    transaction_type: TransactionType
    quantity: int
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── History (for listing transactions) ────────────────────
class StockTransactionHistory(BaseModel):
    id: int
    transaction_type: TransactionType
    quantity: int
    notes: Optional[str] = None
    employee: Optional[EmployeeBasic] = None 
    created_at: datetime

    class Config:
        from_attributes = True