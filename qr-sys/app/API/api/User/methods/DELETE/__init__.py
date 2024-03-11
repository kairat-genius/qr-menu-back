from ......framework import app, jwt, delete_user_email, Person
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ResponseModels.Recovery import ResponseCheckRecovery as ResponseCheckDelete
from .....ValidationModels.DeleteUser import DeleteUser
from ......settings import COOKIE_KEY
from .....tags import USER


@app.delete('/api/admin/delete/session/user', tags=[USER], dependencies=[Depends(jwt)])
async def delete_user_from_session():
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
async def delete_user(data: DeleteUser, hashf: str = Depends(jwt)) -> ResponseCheckDelete:

    """
    <h1>Повністью видаляє користувача з системи</h1>
    """

    user = await Person(hashf).initialize()
    email, code = user.email, data.code

    if code == delete_user_email[email]:
        
        await user.delete_user()
        del delete_user_email[email]

        response = JSONResponse(status_code=200, content={"msg": "Користувача видаленно з системи"})
        response.delete_cookie(COOKIE_KEY, secure=True, samesite="none")

        return response

    else:
        raise HTTPException(status_code=400, detail="Неверный код для удаления пользователя")