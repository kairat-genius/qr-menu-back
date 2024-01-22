# FastAPI application


Встановити всі залежності 

> pip install -r requirements.txt


Для того щоб ініціалізувати базу данних 
та створити всі таблиці 

> alembic revision --autogenerate -m "<інфо про міграцію>" 
> alembic upgrade head


Запуск додатку 

> uvicorn app.API.api:app



Файлова система проекту:

- app
    - API 
        - ValidationModels
            - models.py        <-- Тут створювати моделі валідації pydentic 

        - api.py               <-- Модуль самого додатку в якому знаходиться наш API
    - database
        - db
            - db_model.py      <-- Модуль з обьектом який взаємодіє з БД

        - tables.py            <-- Модуль для створення таблиць

    - framework
        - trash_methods 
            - trash.py         <-- Модуль для створення інших методів 

    - settings.py              <-- Конфігурація додатку  