from .....database.tables import (restaurant, categories, 
                                  dishes, ingredients)
from fastapi.exceptions import HTTPException
from fastapi import status
from .....framework import app, db, logger
from .....settings import CLIENT_MENU_LINK
import os


menu_link = os.environ.get(
    "CLIENT_MENU_LINK",
     CLIENT_MENU_LINK
)

@app.get(menu_link)
async def client_get_restaurant_menu(
    rest: str,
    id: int,
    table: int
):
    func_name = client_get_restaurant_menu.__name__

    try:
        get_rest: dict = await db.async_get_where(
            restaurant, 
            and__=(
                restaurant.c.id == id,
                restaurant.c.name == rest
            ), 
            all_=False,
            to_dict=True
        )
    except Exception as e:
        logger.error(f"\nfunc: {func_name}\n" / 
                     f"Error: {e}")
        
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Невідома помилка під час обробки транзакції."
        )
    
    if ~isinstance(get_rest, dict):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Данний заклад відсутній в системі."
        )
    
    del get_rest["hashf"]
    rest_id: int = get_rest.pop("id")

