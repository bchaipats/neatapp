from dataclasses import dataclass
from typing import Optional

@dataclass
class Restaurant:
    restaurant: Optional[str] = None
    food: Optional[str] = None
    discount: Optional[str] = None
    price: Optional[str] = None
    rating: Optional[str] = None
    review: Optional[str] = None