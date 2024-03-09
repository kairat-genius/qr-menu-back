from ......framework import app, jwt, db, logger, delete_user_email
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Recovery import ResponseCheckRecovery as ResponseCheckDelete
from .....ValidationModels.Recovery import Recovery as Delete_user
from ......database.tables import authefication
from ......settings import COOKIE_KEY
from .....tags import USER


@app.delete('/api/admin/delete/session/user', tags=[USER])
async def delete_user_from_session(_: None = Depends(jwt)):
    """
    <h1>Вихід користувача з системи</h1>

    <p>Якщо потрібно вийти з аккаунту користувача потрібно відправити DELETE
    запит на цей url та обов'язково повинен бути токен в cookie. В іншому випадку
    буде помилка.</p>
    """
    response = JSONResponse(status_code=200, content={"msg": "Користувача видалено з сессії"})
    response.delete_cookie(COOKIE_KEY, secure=True, samesite="none")

    return response

@app.delete('/api/admin/delete/user', tags=[USER])
async def delete_user(data: Delete_user, hashf: str = Depends(jwt)) -> ResponseCheckDelete:

    """
    <h1>Повністью видаляє користувача з системи</h1>
    """

    email, _, code = *data.email, data.code


    if code == delete_user_email[email]:

        try: 
            await db.async_delete_data(authefication, exp=authefication.c.hashf == hashf)
            del delete_user_email[email]
        except Exception as e:
            logger.error(f"Помилка під час видалення користувача\n\nhashf: {hashf}\nError: {e}")
            raise HTTPException(status_code=500, detail="Невідома помилка під час виконання операції")
        else:
            response = JSONResponse(status_code=200, content={"msg": "Користувача видаленно з системи"})
            response.delete_cookie(COOKIE_KEY, secure=True, samesite="none")

            return response
        

    else:
        raise HTTPException(status_code=400, detail="Неверный код для удаления пользователя")