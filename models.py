from typing import TypedDict


class Restaurant(TypedDict):
    name: str
    cuisines: str
    rating: float | int | str
    address: str