from .....ResponseModels.Category import GetCategories
from ......framework import app, jwt, Person
from .....tags import CATEGORY

from fastapi.responses import JSONResponse
from fastapi import Depends



@app.get('/api/admin/get/categories', tags=[CATEGORY])
async def get_categories(hashf: str = Depends(jwt)) -> GetCategories:

    user = await Person(hashf=hashf).initialize()

    restaurant = await user.get_restaurant()
    category = await restaurant.get_categories()
    
    return JSONResponse(status_code=200, content={'categories': [i.get_data() for i in category]})


