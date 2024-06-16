from .....ResponseModels.Register import RegisterResponseFail
from ......framework import app, jwt, Person
from .....tags import DISHES

from fastapi.responses import JSONResponse
from fastapi import Depends


@app.delete('/admin/delete/dish', tags=[DISHES])
async def delete_dish(dish_id: int, category_id: int, hashf: str = Depends(jwt)) -> RegisterResponseFail:
    dish, category = dish_id, category_id

    user = await Person(hashf=hashf).initialize()

    restaurant = await user.get_restaurant()

    await restaurant.delete_dish(
        category_id=category,
        dish_id=dish
    ) 

    return JSONResponse(status_code=200, content={'msg': f'Страва id: {dish} видаленна успішно з категорії id: {category}'})