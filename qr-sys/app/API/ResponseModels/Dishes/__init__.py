from ...ValidationModels.Dishes import Dish, DishUpdate
from pydantic import BaseModel
from typing import Optional

class DishResponse(Dish):
    id: int

class DishData(DishUpdate):
    id: int



