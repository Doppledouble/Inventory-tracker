from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.location import Location
from schemas.location import LocationCreate, LocationUpdate

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.post("/")
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    new_location = Location(
        city            = location.city,
        location_name   = location.location_name,
        description     = location.description
    )
    
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    
    return new_location


@router.get("/")
def get_locations(db:Session = Depends(get_db)):
    return db.query(Location).all()


@router.get("/{location_id}")
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location


@router.patch("/{location_id}")
def update_location(location_id: int, location_data: LocationUpdate, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()

    if not location:
        raise HTTPException(status_code=404, detail="location not found")

    update_data = location_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(location, key, value)

    db.commit()
    db.refresh(location)

    return location


@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()

    if location:
        db.delete(location)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Location not found")
        
    return {"message": "deleted"}

