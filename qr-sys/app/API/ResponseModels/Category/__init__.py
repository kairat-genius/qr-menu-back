from pydantic import BaseModel
from typing import List


class CategoryTable(BaseModel):
    id: int
    category: str
    color: List[int]
    restaurant_id: int


class GetCategories(BaseModel):
    categories: List[CategoryTable]