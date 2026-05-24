from fastapi import FastAPI

from database import Base, engine
from models.item import Item
from models.location import Location
from models.employee import Employee
from models.assignment import Assignment
from routes import item, location, employee, assignment

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory API",
    version="1.0.0"
)

app.include_router(item.router)
app.include_router(location.router)
app.include_router(employee.router)
app.include_router(assignment.router)


@app.get("/")
def root():
    return {"message": "Inventory API is running"}