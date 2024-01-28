**QR-sys FastAPI backend app**


# По етапний гайд як ініціалізувати додаток вручу

1. Встановлення всіх залежностей 

```bash
user@~: pip install -r requirements.txt
```

2. Ініціалізація бази данних та створення всіх таблиць

```bash
user@~: alembic revision --autogenerate
user@~: alembic upgrade head
```

3. Запуск додатку

```bash
user@~: uvicorn app.API.api:app --host:<host> --port:<port>
```

* Або можете запустити додаток за допомогою *Dockerfile*


# Файлова система проекту

- app
    - API
        - api <-- Головна папка з функціями нашого API
            ...
        - QR <-- Обьект для взаємодії з QR, генерація, видалення, збереження, отримання
            ...
        - ResponseModels <-- pydantic моделі для валідації исходящих відповідей від серверу
            ...
        - ValidationModels <-- pydantic моделі для валідації входящих запитів від клієнту
            ...

    - database 
        - db
            - Meta <-- Створення метаданних для бази данних та підключення
                ...
            - models
                - db_model.py <-- Обьєкт через який відбувається взаємодія з базою данних
            
            - TablesParse <-- Філтрує обьєкти таблиць  
                ... 

        - tables.py <-- Тут описуються всі таблиці додатку для їх створення треба використовувати alembic

    - framework
        - JWT
            - JWTCache <-- Каталог який зберігає кешовані JWT ключи та декоратори які взаємодіють з кешованими токенами
                ...
            - MetaData
                - jwt_metadata.py <-- Обьєкт через який відбувається взаємодія з JWT хешованимим токенами (отримання, видалення)
            - token 
                - auth.py <-- Обьєкт який створює та перевіряє дійсність JWT токенів, також через нього
                                відбувається взаємодія з каталогом MetaData
            - validation <-- Перевіряє входящі токени в запиті та валідує їх також повертає токен якщо він дійсний 
                ...
            - trash_methods
                - trash.py <-- Обьєкт для методів які незнаєш куди пихнути

    - settings.py <-- Налаштування для проекту