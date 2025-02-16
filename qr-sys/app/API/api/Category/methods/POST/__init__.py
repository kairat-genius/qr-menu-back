from .....ValidationModels.Category import CategorySet
from .....ResponseModels.Category import CategoryTable
from ......framework import app, jwt, Person
from .....tags import CATEGORY
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException

# Імпортуємо логування
import logging
from configLogging import configure_logging

# Налаштування директорії та назви для файлу з логами
configure_logging("/Users/andruuy/Documents/Study/qr-menu-back/qr-sys/app/API/api/Category/methods/POST", "add_category.log")

@app.post('/admin/add/category', tags=[CATEGORY])
async def add_category(data: CategorySet, hashf: str = Depends(jwt)) -> CategoryTable:
    try:
        # Логування отриманих даних
        logging.info(f"Received data: {data}")

        user = await Person(hashf=hashf).initialize()
        logging.info(f"User initialized: {user}")

        restaurant = await user.get_restaurant()
        logging.info(f"Restaurant retrieved: {restaurant}")

        new_category = await restaurant.add_category(**data.model_dump())
        logging.info(f"Category added successfully: {new_category}")

        return JSONResponse(status_code=200, content=new_category.get_data())
    except Exception as e:
        logging.error(f"Error adding category: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error adding category: {str(e)}")
