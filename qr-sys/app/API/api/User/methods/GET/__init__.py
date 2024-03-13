from ......framework import jwt, app, db, logger, Person
from .....ResponseModels.Register import RegisterUserData
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from ......database.tables import tables
from fastapi import Depends
from .....tags import USER


@app.get("/api/admin/login/token", tags=[USER])
async def login_by_token(hashf: str = Depends(jwt)) -> RegisterUserData:

    """
    <h1>Логування в систему за допомогою JWT токену</h1>
    <p><strong>Щоб отримати данні користувача</strong> та виконати успішне логування у користувача в 
    <strong>cookie</strong> повинен знаходитись JWT токен. Він повинен бути дійсним та мати <strong>ключ token</strong> </p>
    """

    try: 
        user = await Person(hashf=hashf).initialize()

        return JSONResponse(status_code=200, content=user.get_parse_data())
    except:
        logger.error(f"JWT {hashf} відстуній в JWTMetaData, але залишається дійсним")
        raise HTTPException(status_code=403, detail='Згенеруйте новий токен для користувача')



@app.get("/api/admin/get-full-info/user", tags=[USER])
async def get_full_info_from_user(hashf: str = Depends(jwt)):
    """
    <h1>Метод для отримання повної інформації про користувача</h1>
    <p>Метод повертає інформацію про аккаунт користувача, заклад, кількість столів та категорії.</p>
    <p>Якщо у користувача <strong>не створений</strong> заклад тоді метод повертає:</p>
    <span>
    <strong>{</strong>
    <br>&nbsp;&nbsp;&nbsp;
    "status": 500,
    <br>&nbsp;&nbsp;&nbsp;
    "details": "Відстунє достатньо інформації"
    <br><strong>}</strong></span>
    
    """

    user = await Person(hashf=hashf).initialize()

    restaurant_data = await user.get_restaurant()

    category = await restaurant_data.get_categories()

    table_count = await db.async_get_where(tables, exp=tables.c.restaurant_id == restaurant_data.id,
                                           all_=False, count=True)



    data = user.get_parse_data() | {"restaurant": restaurant_data.get_data() 
                                 |         {"categories": [i.get_data() for i in category]}
                                 |         {"tables_count": table_count[0] if table_count else 0}
                                 }

    
    return JSONResponse(status_code=200, content=data)