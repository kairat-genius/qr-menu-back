from .....ResponseModels.Register import RegisterResponseFail
from .....ValidationModels.Recovery import RecoveryPassword
from ......framework import app, t, Person
from fastapi.responses import JSONResponse
from .....tags import USER


@app.put("/api/admin/recovery/password", tags=[USER])
async def recovery_password(data: RecoveryPassword) -> RegisterResponseFail:

    """
    <h1>Встановлює новий пароль для користувача</h1>
    """

    user_id, password = data.id, t.get_hash(data.password)

    user = await Person(id=user_id).initialize()
    
    await user.update_user_data(password=password)
    
    return JSONResponse(status_code=200, content={"msg": "Пароль для користувача змінено"})