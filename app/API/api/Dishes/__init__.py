from ....framework import app, jwt_validation, db, logger
from fastapi import Depends

from ...ValidationModels.Dishes import DishAdd, DishDelete
from ...ResponseModels.Dishes import DishResponse
from ...ResponseModels.Register import RegisterResponseFail

from ....database.tables import dishes


TAG = "Dishes"

@app.post('/api/admin/add/dish', tags=[TAG])
async def add_dish(data: DishAdd, token: str = Depends(jwt_validation)) -> (DishResponse | RegisterResponseFail):

    insert_data = data.data.model_dump()

    try: new_dish = db.insert_data(dishes, **insert_data)
    except Exception as e:
        logger.error(f"Помилка при додавані страви\n\nСессія: {token[:10]}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час виконання'}
    
    return {'status': 200, 'dish': new_dish._asdict()}


@app.get('/api/admin/get/dish/{category_id}', tags=[TAG], dependencies=[Depends(jwt_validation)])
async def get_dishes(category_id: int) -> (DishResponse | RegisterResponseFail):
    try: data = db.get_where(dishes, exp=dishes.c.category_id == category_id, 
                                to_dict=True)
    except Exception as e:
        logger.error(f"Помилка під час отримання страв\n\nid Категорії: {category_id}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час обробки транзакції'}
    

    return {'status': 200, 'dish': data}
    

@app.delete('/api/admin/delete/dish', tags=[TAG], dependencies=[Depends(jwt_validation)])
async def delete_dish(data: DishDelete) -> RegisterResponseFail:
    dish, category = data.dish_id, data.category_id

    try: db.delete_data(dishes, and__=(dishes.c.id == dish,
                                        dishes.c.category_id == category))
    except Exception as e:
        logger.error(f"Помилка під час видалення страви id: {dish} з категорії id: {category}\n\nError: {e}")
        return {'status': 500, 'msg': 'Невідома помилка під час видалення страви'}
    

    return {'status': 200, 'msg': f'Страва id: {dish} видаленна успішно з категорії id: {category}'}