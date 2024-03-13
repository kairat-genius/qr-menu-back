from .....settings import CLIENT_MENU_LINK
from .....framework import app, Restaurant
from fastapi.responses import JSONResponse
from ....tags import CLIENT
from fastapi import status
import os


menu_link = os.environ.get(
    "CLIENT_MENU_LINK",
     CLIENT_MENU_LINK
)

@app.get(menu_link, tags=[CLIENT])
async def client_get_restaurant_menu(
    restaurant: str,
    id: int,
    table: int
):
    restaurant_table = await Restaurant(
        id=id,
        name=restaurant
    ).initialize()

    restaurant_data = await restaurant_table.get_full_data(id=True)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=restaurant_data
    )
