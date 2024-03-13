from ......framework import app, jwt, Person
from .....ResponseModels.Dishes import Dish
from .....tags import DISHES
from typing import List

from fastapi.responses import JSONResponse
from fastapi import Depends


@app.get('/api/admin/get/dish', tags=[DISHES])
async def get_dishes(category_id: int, hashf: str = Depends(jwt)) -> List[Dish]:

    user = await Person(hashf=hashf).initialize()

    restaurant = await user.get_restaurant()

    dishes = await restaurant.get_dishes(category_id)

    return JSONResponse(status_code=200, content=[i.get_data() for i in dishes])