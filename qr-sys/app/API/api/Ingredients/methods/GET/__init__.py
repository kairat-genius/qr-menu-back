from ......framework import app, jwt, db, logger, Person
from .....ResponseModels.Ingredients import Ingredient
from .....tags import INGREDIENTS
from typing import List

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends


@app.get('/api/admin/get/ingredients', tags=[INGREDIENTS])
async def get_ingredients(dish_id: int, hashf: str = Depends(jwt)) -> List[Ingredient]:

    user = await Person(hashf).initialize()

    restaurant = await user.get_restaurant()

    ingredients = await restaurant.get_ingredients(dish_id)

    return JSONResponse(status_code=200, content=[i for i in ingredients])