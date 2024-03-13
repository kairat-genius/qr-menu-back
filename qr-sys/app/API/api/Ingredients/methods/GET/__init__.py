from ......framework import app, jwt, Person
from .....ResponseModels.Ingredients import Ingredient
from .....tags import INGREDIENTS
from typing import List

from fastapi.responses import JSONResponse
from fastapi import Depends


@app.get('/api/admin/get/ingredients', tags=[INGREDIENTS])
async def get_ingredients(dish_id: int, hashf: str = Depends(jwt)) -> List[Ingredient]:

    user = await Person(hashf=hashf).initialize()

    restaurant = await user.get_restaurant()

    ingredients = await restaurant.get_ingredients(dish_id)

    return JSONResponse(status_code=200, content=[i.get_data() for i in ingredients])