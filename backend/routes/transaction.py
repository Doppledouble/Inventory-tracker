from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.item import Item
from models.transaction import Transaction
from models.enums import TransactionType

from schemas.transaction import (
    StockAdd,
    StockRemove,
    StockAdjustment
)

router = APIRouter(prefix="/transactions",tags=["Transactions"])

# Addition type transaction because of purchacing
@router.post("/items/{item_id}/add")
def add_stock(item_id: int, stock: StockAdd, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item: raise HTTPException(status_code=404, detail="Item not found")

    item.count += stock.quantity

    transaction = Transaction(
        item_id=item.id,
        quantity=stock.quantity,
        transaction_type=TransactionType.PURCHASE,
        notes=stock.notes
    )

    db.add(transaction)

    db.commit()
    db.refresh(item)
    
    return {
    "message": "Stock added successfully",
    "current_stock": item.count
    }
    
# Remove type transaction because of damaged items    
@router.post("/items/{item_id}/remove")
def remove_stock(item_id: int, stock: StockRemove, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item: raise HTTPException(status_code=404, detail="Item not found")
    
    if item.count < stock.quantity: raise HTTPException(status_code=400,detail="Insufficient stock")

    item.count -= stock.quantity

    transaction = Transaction(
        item_id=item.id,
        quantity=-stock.quantity,
        transaction_type=TransactionType.DAMAGE,
        notes=stock.notes
    )

    db.add(transaction)

    db.commit()

    return {
        "message": "Stock removed successfully"
    }

# Required item stock adjustment IF NEEDED ONLY
@router.post("/items/{item_id}/adjust")
def adjust_stock(item_id: int, adjustment: StockAdjustment, db: Session = Depends(get_db)):
    item = (db.query(Item).filter(Item.id == item_id).first())

    if not item: raise HTTPException(status_code=404, detail="Item not found")

    difference = adjustment.new_count - item.count

    if difference == 0:
        raise HTTPException(status_code=400, detail="No adjustment needed")

    item.count = adjustment.new_count

    transaction = Transaction(
        item_id=item.id,
        quantity=difference,
        transaction_type=TransactionType.ADJUSTMENT,
        notes=adjustment.notes
    )

    db.add(transaction)

    db.commit()
    db.refresh(item)

    return {
        "message": "Stock adjusted successfully",
        "previous_count": adjustment.new_count - difference,
        "new_count": item.count,
        "difference": difference
    }
    
# get all item's transaction history    
@router.get("/items/{item_id}/history")
def get_item_history(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return (
        db.query(Transaction).filter(Transaction.item_id == item_id).order_by(Transaction.created_at.desc()).all()
    )

# get all transactions of all items
@router.get("/")
def get_transactions(
    db: Session = Depends(get_db)
):
    return (
        db.query(Transaction)
        .order_by(Transaction.created_at.desc())
        .all()
    )