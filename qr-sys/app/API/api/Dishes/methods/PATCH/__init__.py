from .....ValidationModels.Dishes import DishUpdate
from .....ResponseModels.Dishes import DishData
from ......framework import app, jwt, Person
from fastapi.responses import JSONResponse
from .....tags import DISHES
from fastapi import Depends

@app.patch('/api/admin/update/dishes', tags=[DISHES])
async def update_dish(dish_id: int, data: DishUpdate, hashf: str = Depends(jwt)) -> DishData:

    new_data = {k: v for k, v in data.model_dump().items() if v}

    user = await Person(hashf=hashf).initialize()

    restaurant = await user.get_restaurant()

    new_dish = await restaurant.update_dish(dish_id, **new_data)

    return JSONResponse(status_code=200, content=new_dish.get_data())


