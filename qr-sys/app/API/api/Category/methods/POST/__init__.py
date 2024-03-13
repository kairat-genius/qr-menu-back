from .....ValidationModels.Category import CategorySet
from .....ResponseModels.Category import CategoryTable
from ......framework import app, jwt, Person
from .....tags import CATEGORY

from fastapi.responses import JSONResponse
from fastapi import Depends


@app.post('/api/admin/add/category', tags=[CATEGORY])
async def add_category(data: CategorySet, hashf: str = Depends(jwt)) -> CategoryTable:

    user = await Person(hashf=hashf).initialize()

    restaurant = await user.get_restaurant()

    new_category = await restaurant.add_category(**data.model_dump())

    return JSONResponse(status_code=200, content=new_category.get_data())