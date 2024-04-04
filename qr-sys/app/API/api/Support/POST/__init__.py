from fastapi import Depends, HTTPException
from ....tags import SUPPORT
from .....framework import jwt, app, logger, Person, send_mail
from ....ValidationModels.Support import EmailSupport
import base64
from fastapi.responses import JSONResponse


@app.post("/api/admin/support/email", tags=[SUPPORT])
async def support(data: EmailSupport, hashf: str = Depends(jwt)) -> dict:
    try:
        user = await Person(hashf=hashf).initialize()

        if data.logo:
            image_content = base64.b64decode(data.logo)
            send_mail.delay(user.email, data.theme, data.body, image_content)
        else:
            send_mail.delay(user.email, data.theme, data.body)



        return JSONResponse(status_code=200, content={"message": "Письмо успешно отправлено! Мы свяжемся с вами в ближайшее время"})

    except Exception as e:
        logger.error(f"Ошибка при отправке электронного письма: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка при отправке электронного письма: {e}")