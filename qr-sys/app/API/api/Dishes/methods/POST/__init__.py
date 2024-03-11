from .....ValidationModels.Dishes import Dish
from ......framework import app, jwt, Person
from .....tags import DISHES

from fastapi.responses import JSONResponse
from fastapi import Depends


@app.post('/api/admin/add/dish', tags=[DISHES])
async def add_dish(data: Dish, hashf: str = Depends(jwt)) -> Dish:

    insert_data = data.model_dump()

    user = await Person(hashf).initialize()

    restaurant = await user.get_restaurant()

    new_dish = await restaurant.add_dish(**insert_data)

    return JSONResponse(status_code=200, content=dict(new_dish))    