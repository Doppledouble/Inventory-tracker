from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models.item import Item
from schemas.item import ItemCreate, ItemUpdate
from models.transaction import Transaction
from models.enums import TransactionType


router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    new_item = Item(
        name=item.name,
        category=item.category,
        count=item.count
    )
    # Insert the new_item first to create the id in the database
    db.add(new_item)
    db.flush()

    transaction = Transaction(
        item_id=new_item.id,
        quantity=item.count,
        transaction_type=TransactionType.ADD
    )
        
    db.add(transaction)
    
    db.commit()
    db.refresh(new_item)

    return new_item


@router.get("/")
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.patch("/{item_id}")
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item_data.model_dump(exclude_unset=True)

    old_count = item.count
    new_count = update_data.get("count", old_count)
    difference = new_count - old_count
    
    for key, value in update_data.items():
        setattr(item, key, value)   
        
    if difference != 0:    
        transaction = Transaction(
            item_id= item.id,
            quantity= difference,
            transaction_type= TransactionType.ADJUSTMENT
        )
        db.add(transaction)

    db.commit()
    db.refresh(item)

    return item


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    transaction = Transaction(
        item_id = item.id,
        quantity =- item.count,
        transaction_type = TransactionType.REMOVE 
    )
    
    db.add(transaction)
    db.delete(item)
    db.commit()

    return {"message": f"Item with id {item_id} successfuly deleted"}