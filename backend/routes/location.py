from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.location import Location
from schemas.location import LocationCreate, LocationUpdate, LocationResponse

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.post("/", response_model=LocationResponse)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    new_location = Location(
        city            = location.city,
        location_name   = location.location_name,
        description     = location.description
    )
    
    existing_location = (
        db.query(Location).filter(
            Location.city == location.city,
            Location.location_name == location.location_name
        ).first()
    )
    
    if existing_location:
        raise HTTPException(status_code=400, detail="Location {location_name}, {city} already exist")
    
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    
    return new_location


@router.get("/", response_model=list[LocationResponse])
def get_locations(db:Session = Depends(get_db)):
    return db.query(Location).all()


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location


@router.patch("/{location_id}",response_model=LocationResponse)
def update_location(location_id: int, location_data: LocationUpdate, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    update_data = location_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(location, key, value)

    db.commit()
    db.refresh(location)

    return location


@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
        
    # if location.items:
    #     raise HTTPException(status_code=400, detail="Cannot delete location with assigned items")
    
    db.delete(location)
    db.commit()    
        
    return {"message": f"Location with id {location_id} successfuly deleted"}

