from .....ResponseModels.Category import GetCategories
from ......framework import app, jwt, Person
from .....tags import CATEGORY

from fastapi.responses import JSONResponse
from fastapi import Depends




@app.get('/api/admin/get/categories', tags=[CATEGORY])
async def get_categories(hashf: str = Depends(jwt)) -> GetCategories:

    user = await Person(hashf).initialize()

    restaurant = await user.get_restaurant()
    category = await restaurant.get_categories()
    
    return JSONResponse(status_code=200, content={'categories': [dict(i) for i in category]})


@app.get("/api/admin/get-full-info/categories", tags=[CATEGORY])
async def get_full_info_categories(hashf: str = Depends(jwt)):

    user = await Person(hashf).initialize()
    restaurant = await user.get_restaurant()
    
    category = await restaurant.get_categories()

    result = {
        **dict(restaurant),
        "categories": [
            {**dict(i), 
                "dishes": [
                    {**dict(j),
                        "ingredients": [
                            dict(l) for l in await j.get_ingredients()
                        ] 
                    } for j in await i.get_dishes()
                ]
            } for i in category 
        ]
    },
    

    
    return JSONResponse(status_code=200, content={"restaurant": result})