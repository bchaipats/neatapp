from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.restaurant.RestaurantOut])
def list_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.restaurant.get_restaurants(db, skip=skip, limit=limit)

@router.get("/{restaurant_id}", response_model=schemas.restaurant.RestaurantOut)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    db_rest = crud.restaurant.get_restaurant(db, restaurant_id)
    if not db_rest:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_rest

@router.post("/", response_model=schemas.restaurant.RestaurantOut, status_code=201)
def create_restaurant(rest: schemas.restaurant.RestaurantCreate, db: Session = Depends(get_db)):
    return crud.restaurant.create_restaurant(db, rest)