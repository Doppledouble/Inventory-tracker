from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models.assignment import Assignment
from models.item import Item
from models.employee import Employee
from models.transaction import Transaction
from models.enums import TransactionType
from schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse

router = APIRouter(prefix="/assignments", tags=["Assignments"])

@router.post("/")
def create_assignment(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    
    #validate item first
    item = db.query(Item).filter(Item.id == assignment.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    # validate employee exists
    employee = (db.query(Employee).filter(Employee.id == assignment.employee_id).first())
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if item.count < assignment.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")    
    
    item.count -= assignment.quantity
    
    new_assignment = Assignment(
        item_id=assignment.item_id,
        employee_id=assignment.employee_id,
        location=assignment.location,
        quantity=assignment.quantity,
        notes=assignment.notes
    )
        
    transaction = Transaction(
        item_id=item.id,
        employee_id=employee.id,
        quantity=-assignment.quantity,
        transaction_type=TransactionType.ASSIGNMENT,
        notes=assignment.notes
    )
    
    
    db.add(new_assignment)
    db.add(transaction)

    db.commit()
    db.refresh(new_assignment)

    return new_assignment


@router.get("/", response_model=list[AssignmentResponse])
def get_assignments(active: bool | None = Query(None, description="Filter by active status"), db: Session = Depends(get_db)):
    query = db.query(Assignment).options(
        joinedload(Assignment.item),
        joinedload(Assignment.employee)
    )
    if active is not None:
        query = query.filter(Assignment.returned_at.is_(None) if active else Assignment.returned_at.isnot(None))

    return query.all()


@router.get("/{assignment_id}")
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    return assignment


@router.patch("/{assignment_id}")
def update_assignment(assignment_id: int, assignment_data: AssignmentUpdate, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    update_data = assignment_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(assignment, key, value)
        
        
    db.commit()
    db.refresh(assignment)

    return assignment


@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if assignment:
        db.delete(assignment)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Assignment not found")
        
    return {"message": f"Assignment with id {assignment_id} successfuly deleted"}


@router.patch("/{assignment_id}/return")
def return_assignment(assignment_id: int,db: Session = Depends(get_db)):
    assignment = (
        db.query(Assignment)
        .filter(Assignment.id == assignment_id).first()
    )

    if not assignment: raise HTTPException(status_code=404, detail="Assignment not found")

    # prevent double return
    if assignment.returned_at: raise HTTPException(status_code=400, detail="Item already returned")

    assignment.returned_at = datetime.now()
    assignment.item.count += assignment.quantity

    transaction = Transaction(
        item_id=assignment.item_id,
        employee_id=assignment.employee_id,
        quantity=assignment.quantity,
        transaction_type=TransactionType.RETURN,
        notes="Item returned"
    )   
    
    db.add(transaction)
    db.commit()
    db.refresh(assignment)

    return {
        "message": "Item returned successfully"
    }