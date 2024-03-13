from .....ValidationModels.Ingredients import IngredientScheme
from ......framework import app, jwt, Person
from .....ResponseModels.Ingredients import Ingredient
from .....tags import INGREDIENTS

from fastapi.responses import JSONResponse
from fastapi import Depends


@app.post('/api/admin/add/ingredient', tags=[INGREDIENTS])
async def add_ingredient(data: IngredientScheme, hashf: str = Depends(jwt)) -> Ingredient:
    ingredient_data, dish_id = data.ingredient, data.dish_id

    user = await Person(hashf=hashf).initialize()

    restaurant = await user.get_restaurant()

    ingredient = await restaurant.add_ingredient(
        dish_id=dish_id, 
        ingredient=ingredient_data
    )
    
    return JSONResponse(status_code=200, content=dict(ingredient))

