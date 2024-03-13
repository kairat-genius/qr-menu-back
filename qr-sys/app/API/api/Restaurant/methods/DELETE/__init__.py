from ......framework import app, jwt, Person
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Register import RegisterResponseFail
from .....tags import RESTAURANT


@app.delete('/api/admin/delete/restaurant', tags=[RESTAURANT])
async def restaurant_delete(hashf: str = Depends(jwt)) -> RegisterResponseFail:

    user = await Person(hashf=hashf).initialize()

    restaurant = await user.get_restaurant()
    await restaurant.delete_restaurant()

    return JSONResponse(status_code=200, content={"msg": 'Ресторан видалений з системи'})