from ......framework import (app, t, jwt, recovery, send_mail, 
                             logger, delete_user_email, Person)

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Depends

from .....ValidationModels.Recovery import ValidationEmail, Recovery
from .....ResponseModels.Register import RegisterResponseFail
from .....ResponseModels.Recovery import ResponseCheckRecovery
from .....ValidationModels.Register import RegisterUser
from .....ValidationModels.Login import LoginByLP
from .....tags import USER, EMAIL



@app.post('/admin/register', tags=[USER])
async def register(data: RegisterUser) -> (RegisterResponseFail):

    hashf = t.get_hash(data.email + data.password)
    password = t.get_hash(data.password)

    get_data = data.model_dump()
    get_data.update(
        hashf=hashf, 
        password=password
    )
    
    time = get_data.pop('time')
    user = Person(**get_data)

    if await user.check_user():
        raise HTTPException(status_code=403, detail=f"{data.email} вже зареєстрований")

    user = await user.add_new_user()

    playload, date, seconds = jwt.get_playload(user.id, user.email, **{time['type']: time['number']})
    token = jwt.get_token(**playload)
    jwt.object.set(token, user.hashf, seconds)

    response = JSONResponse(status_code=200, content={"msg": "Користувача зарєстровано"})
    response.set_cookie(**jwt.cookie_params(token, date))
    return response


@app.post("/admin/login", tags=[USER])
async def login(data: LoginByLP) -> RegisterResponseFail:

    email, password, time_type, time = data.email, t.get_hash(data.password), data.time.type, data.time.number
    user = await Person(email=email).initialize()

    if password != user.password:
        raise HTTPException(status_code=403, detail=f"Хибний пароль для {email}")

    # Генеруємо новий токен, зберігаємо та повертаємо дані
    playload, date, seconds = jwt.get_playload(user.id, user.email, **{time_type: time})
    token = jwt.get_token(**playload)
    jwt.object.set(token, user.hashf, seconds)

    response = JSONResponse(status_code=200, content={"msg": "Вхід в систему успішний"})
    response.set_cookie(**jwt.cookie_params(token, date))

    return response
    


@app.post('/admin/set/recovery/code', tags=[USER, EMAIL])
async def set_recovery_code(data: ValidationEmail) -> RegisterResponseFail:

    """
    <h1>Встановлення коду для відновлення</h1>
    <p>Метод створює код для відновлення паролю та надсилає його на пошту користувача яка вказана в тілі запиту</p>
    """

    user = await Person(email=data.email).initialize()
    email = user.email

    code = recovery.set_code()

    recovery[email] = code

    try:
        msg = f"""If you don't request code for recovery, ignore this mail.\nYour code for recovery: {code}"""
        send_mail.delay(email, "Restaurant QR-system recovery account", msg)
        return JSONResponse(status_code=200, content={"msg": "Повідомлення надіслано"})

    except Exception as e:
        del recovery[email]
        logger.error(f"Помилка під час відправки email.\n\nEmail: {email}\nError: {e}")
        raise HTTPException(status_code=500, detail="Невідома помилка під час обробки транзакії")


@app.post("/admin/recovery/code/check", tags=[USER])
async def recovery_code_check(data: Recovery) -> ResponseCheckRecovery:

    """
    <p>Метод перевіряє код який надіслав користувач та якщо код дійсний повертає стасус 200</p>
    """

    email, code = data.email, data.code 

    user = await Person(email=email).initialize()

    if code == recovery[email]:
        del recovery[email]
        return JSONResponse(status_code=200, content={"msg": "Код дійсний.", "id": user.id})
    
    raise HTTPException(status_code=403, detail="Введений код не дійсний")


@app.post("/admin/set/delete/code", tags=[USER, EMAIL])
async def delete_email_code(hashf: str = Depends(jwt)) -> RegisterResponseFail:
    
    user = await Person(hashf=hashf).initialize()
    email = user.email

    code = delete_user_email.set_code()
    delete_user_email[email] = code

    try:
        msg = f"""If you don't want to delete your account, please ignore this mail.\nYour deletion code: {code}"""
        send_mail.delay(email, "Restaurant QR-system account deletion", msg)
        return JSONResponse(status_code=200, content={"msg": "Код отправлен в почту"})

    except Exception as e:
        del recovery[email]
        logger.error(f"Ошибка при отправке email.\n\nEmail: {email}\nError: {e}")
        raise HTTPException(status_code=500, detail="Неизвестная ошибка при обработке транзакии")