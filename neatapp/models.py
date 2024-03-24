from pydantic import BaseModel


class Restaurant(BaseModel):
    """Data model for an restaurant."""

    restaurant: str
    food: str
    discount: str
    price: str
    rating: str
    review: str
