from pydantic import BaseModel


class Ingredient(BaseModel):
    id: int
    ingredient: str
    dish_id: int
    restaurant_id: int
