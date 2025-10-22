from pydantic import BaseModel

class RestaurantBase(BaseModel):
    name: str
    description: str | None = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantOut(RestaurantBase):
    id: int
    class Config:
        orm_mode = True