from pydantic import BaseModel, Field, validator
from enum import Enum

from random import randint
from typing import Tuple


class CategorySet(BaseModel):
    category: str
    color: str

class CategoryDelType(str, Enum):
    all = "all"
    category = "category"