from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models.item import Item
from models.transaction import Transaction

from schemas.transaction import StockTransactionResponse, StockTransactionHistory

router = APIRouter(prefix="/transactions",tags=["Transactions"])

# get all item's transaction history    
@router.get("/items/{item_id}/history", response_model=list[StockTransactionHistory])
def get_item_history(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return (
        db.query(Transaction)
        .options(joinedload(Transaction.employee))  # avoid N+1
        .filter(Transaction.item_id == item_id)
        .order_by(Transaction.created_at.desc())
        .all()
    )

# get all transactions of all items
@router.get("/", response_model=list[StockTransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    return (
        db.query(Transaction)
        .options(
            joinedload(Transaction.item),
            joinedload(Transaction.employee)
        )
        .order_by(Transaction.created_at.desc())
        .all()
    )