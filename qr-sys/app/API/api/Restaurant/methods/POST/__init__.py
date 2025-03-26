from .....ValidationModels.Restaurant import RestaurantRegister
from .....ResponseModels.Restaurant import RestaurantData
from ......framework import app, jwt, Person
from .....tags import RESTAURANT

from fastapi.responses import JSONResponse
from fastapi import Depends


@app.post('/admin/add/restaurant', tags=[RESTAURANT])
async def restaurant_add(data: RestaurantRegister, hashf: str = Depends(jwt)) -> RestaurantData:

    """
    
    <h1>Створення закладу користувача</h1>
    <br>
    <p>Для використання цього та наступних методів у вас вже <strong>повинен</strong> бути в cookie JWT токен</p>
    
    """

    restaurant_data = data.model_dump()

    user = await Person(hashf=hashf).initialize()

    restaurant = await user.add_restaurant(**restaurant_data)

    return JSONResponse(status_code=200, content=restaurant.get_data())


