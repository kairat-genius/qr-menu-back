from .....ValidationModels.Restaurant import RestaurantUpdate, RestaurantDataDelete
from .....ResponseModels.Restaurant import RestaurantData
from ......framework import app, jwt, Person
from fastapi.responses import JSONResponse
from .....tags import RESTAURANT
from fastapi import Depends


@app.patch('/api/admin/update/restaurant', tags=[RESTAURANT])
async def restaurant_data_update(data: RestaurantUpdate, hashf: str = Depends(jwt)) -> RestaurantData:

    new_data = {k: v for k, v in data.model_dump().items() if v}

    user = await Person(hashf=hashf).initialize()
    restaurant = await user.get_restaurant()

    restaurant.update_attr(**new_data)
    await restaurant.update_restaurant()

    return JSONResponse(status_code=200, content=restaurant.get_data())


@app.patch("/api/admin/delete/data", tags=[RESTAURANT])
async def delete_restaurant_data(data: RestaurantDataDelete, hashf: str = Depends(jwt)) -> RestaurantData:
    
    """
    <h1>Якщо ключ має значення true тоді це поле буде видаленно з БД</h1>
    """

    user = await Person(hashf=hashf).initialize()
    restaurant = await user.get_restaurant()

    data_to_delete = data.model_dump()
    parse_data = [i for i in data_to_delete if data_to_delete.get(i)]

    await restaurant.delete_data(*parse_data)

    return JSONResponse(status_code=200, content=restaurant.get_data())