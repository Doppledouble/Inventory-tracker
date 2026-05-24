from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.employee import Employee
from schemas.employee import EmployeeCreate, EmployeeUpdate

router = APIRouter(prefix="/employee", tags=["Employee"])

@router.post("/")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(
        first_name  = employee.first_name,
        last_name   = employee.last_name,
        email       = employee.email,
        is_admin    = employee.is_admin
    )
    
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    
    return new_employee


@router.get("/")
def get_employees(db:Session = Depends(get_db)):
    return db.query(Employee).all()


@router.get("/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


@router.patch("/{employee_id}")
def update_employee(employee_id: int, employee_data: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = employee_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if employee:
        db.delete(employee)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    return {"message": "deleted"}