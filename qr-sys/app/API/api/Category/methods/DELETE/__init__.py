from .....ResponseModels.Register import RegisterResponseFail
from .....ValidationModels.Category import CategoryDelType
from ......framework import app, jwt, Person
from .....tags import CATEGORY
from fastapi import status

from fastapi.responses import JSONResponse
from fastapi import Depends


@app.delete('/admin/delete/categories', tags=[CATEGORY])
async def delete_categories(type: CategoryDelType, category_id: int = 0, hashf: str = Depends(jwt)) -> RegisterResponseFail:

    """
    <h3>Видалення категорії аналогічно як зі столами також можете вказати "all" або "category" та конкретний id категорії</h3>
    
    """

    user = await Person(hashf=hashf).initialize()

    restaurant = await user.get_restaurant()

    msg = await restaurant.delete_category(type, category_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"msg": msg}
    )