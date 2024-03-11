from ......framework import app, jwt, Person
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Restaurant import RestaurantData
from .....tags import RESTAURANT


@app.get('/api/admin/get/restaurant', tags=[RESTAURANT])
async def get_restaurant(hashf: str = Depends(jwt)) -> RestaurantData:

    user = await Person(hashf).initialize()

    restaurant = await user.get_restaurant()

    return JSONResponse(status_code=200, content=dict(restaurant))