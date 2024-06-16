from .....ResponseModels.Register import RegisterResponseFail
from ......framework import app, jwt, Person
from .....tags import INGREDIENTS

from fastapi.responses import JSONResponse
from fastapi import Depends


@app.delete("/admin/delete/ingredients", tags=[INGREDIENTS])
async def delete_ingredients(ingredient_id: int, dish_id: int, hashf: str = Depends(jwt)) -> RegisterResponseFail:

    user = await Person(hashf=hashf).initialize()

    restaurant = await user.get_restaurant()

    await restaurant.delete_ingredient(ingredient_id, dish_id)

    return JSONResponse(status_code=200, content={"msg": f"Інгредіент id: {ingredient_id} успішно видаленний"})    