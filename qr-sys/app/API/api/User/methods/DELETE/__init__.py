from ......framework import app, jwt_validation, db, logger, delete_user_email
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import Depends
from .....ResponseModels.Recovery import ResponseCheckRecovery as ResponseCheckDelete
from .....ResponseModels.Register import RegisterResponseFail
from ......database.tables import authefication
from .....tags import USER
from .....ValidationModels.Recovery import Recovery as Delete_user


@app.delete('/api/admin/delete/session/user', tags=[USER], dependencies=[Depends(jwt_validation)])
async def delete_user_from_session():
    """
    <h1>Вихід користувача з системи</h1>

    <p>Якщо потрібно вийти з аккаунту користувача потрібно відправити DELETE
    запит на цей url та обов'язково повинен бути токен в cookie. В іншому випадку
    буде помилка.</p>
    """

@app.delete('/api/admin/delete/user', tags=[USER])
async def delete_user(hashf: str = Depends(jwt_validation)) -> RegisterResponseFail:

    """
    <h1>Повністью видаляє користувача з системи</h1>
    """

    try: await db.async_delete_data(authefication, exp=authefication.c.hashf == hashf)
    except Exception as e:
        logger.error(f"Помилка під час видалення користувача\n\nhashf: {hashf}\nError: {e}")
        raise HTTPException(status_code=500, detail="Невідома помилка під час виконання операції")
    
    return JSONResponse(status_code=200, content={"msg": "Користувача видаленно з системи"})


@app.delete('/api/admin/delete_code/user', tags=[USER])
async def delete_code_user(hashf: str = Depends(jwt_validation), data: Delete_user = None) -> ResponseCheckDelete:

    email, code = data.email[0], data.code

    try:
        if not code:
            return JSONResponse(status_code=400, content={"msg": "Необходим код для удаления пользователя"})

        user = await db.async_get_where(authefication, exp=authefication.c.hashf == hashf, all_=False, to_dict=True)

        if user is None:
            return JSONResponse(status_code=404, content={"msg": "Пользователь не найден"})

        if code == delete_user_email[email]:
            del delete_user_email[email]
            await db.async_delete_data(authefication, exp=authefication.c.hashf == hashf)
            return JSONResponse(status_code=200, content={"msg": "Пользователь удален"})
        else:
            return JSONResponse(status_code=400, content={"msg": "Неверный код для удаления пользователя"})

    except Exception as e:
        logger.error(f"Ошибка при удалении пользователя\n\nhashf: {hashf}\nError: {e}")
        return JSONResponse(status_code=500, content={"msg": f"Произошла ошибка при удалении пользователя {e}, {email}, {code}"})
