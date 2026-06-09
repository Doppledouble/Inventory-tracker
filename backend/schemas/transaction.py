from pydantic import BaseModel
from typing import Optional


class StockAdd(BaseModel):
    quantity: int
    notes: Optional[str] = None


class StockRemove(BaseModel):
    quantity: int
    notes: Optional[str] = None
    

class StockAdjustment(BaseModel):
    quantity: int
    notes: Optional[str] = None    
