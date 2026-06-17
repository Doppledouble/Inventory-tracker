from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models.item import Item
from models.transaction import Transaction
from models.enums import TransactionType

from schemas.transaction import StockTransactionRequest, StockTransactionResponse, StockTransactionHistory, StockAdjustmentRequest

router = APIRouter(prefix="/transactions",tags=["Transactions"])

# Addition type transaction because of purchacing
@router.post("/items/{item_id}/add", response_model=StockTransactionResponse)
def add_stock(item_id: int, stock: StockTransactionRequest, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item: 
        raise HTTPException(status_code=404, detail="Item not found")

    item.count += stock.quantity

    transaction = Transaction(
        item_id=item.id,
        quantity=stock.quantity,
        transaction_type=TransactionType.PURCHASE,
        employee_id = stock.employee_id,
        notes=stock.notes
    )

    db.add(transaction)

    db.commit()
    db.refresh(transaction)
    
    return transaction
    
# Remove type transaction because of damaged items    
@router.post("/items/{item_id}/remove", response_model=StockTransactionResponse)
def remove_stock(item_id: int, stock: StockTransactionRequest, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item: 
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.count < stock.quantity: 
        raise HTTPException(status_code=400,detail="Insufficient stock")

    item.count -= stock.quantity

    transaction = Transaction(
        item_id=item.id,
        quantity=-stock.quantity,
        transaction_type=TransactionType.DAMAGE,
        employee_id = stock.employee_id,
        notes=stock.notes
    )

    db.add(transaction)

    db.commit()

    db.refresh(transaction)
    
    return transaction

# Required item stock adjustment IF NEEDED ONLY
@router.post("/items/{item_id}/adjust", response_model=StockTransactionResponse)
def adjust_stock(item_id: int, stock: StockAdjustmentRequest, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if stock.new_quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")

    if stock.new_quantity == item.count:
        raise HTTPException(status_code=400, detail="No adjustment needed, quantity is already the same")

    difference = stock.new_quantity - item.count  
    item.count = stock.new_quantity               

    transaction = Transaction(
        item_id=item.id,
        quantity=difference,       
        transaction_type=TransactionType.ADJUSTMENT,
        employee_id=stock.employee_id,
        notes=stock.notes
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction
    
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