from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.assignment import Assignment
from models.item import Item
from models.employee import Employee
from schemas.assignment import AssignmentCreate, AssignmentUpdate

router = APIRouter(prefix="/assignment", tags=["Assignment"])

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
    
    # prevent double active assignment
    existing_assignment = (db.query(Assignment).filter(
        Assignment.item_id == assignment.item_id,
        Assignment.returned_at.is_(None)).first()
    )
    if existing_assignment:
        raise HTTPException(
            status_code=400,
            detail="Item is already assigned"
        )
    
    new_assignment = Assignment(
        item_id  = assignment.item_id,
        employee_id   = assignment.employee_id,
        notes       = assignment.notes    
    )
    
    item.status = "assigned"
    
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    return new_assignment


@router.get("/")
def get_assignments(db: Session = Depends(get_db)):
    return db.query(Assignment).all()


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
        
    return {"message": "deleted"}