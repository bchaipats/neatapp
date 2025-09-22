from dataclasses import dataclass

@dataclass
class Restaurant:
    id: int
    name: str
    cuisine: str
    location: str