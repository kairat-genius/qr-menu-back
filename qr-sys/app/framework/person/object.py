from ...database.tables import (authefication, restaurant)
from ...database.db.models._async import async_db
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from .restaurant import Restaurant
from ...settings import logger
from fastapi import status


class Person(async_db):
    id: int
    hashf: str
    email: str
    password: str

    def __init__(self, hashf: str) -> None:
        super().__init__()
        setattr(self, "hashf", hashf)
    
    async def initialize(self):
        user: dict = await self.async_get_where(
            instance=authefication,
            exp=authefication.c.hashf == self.hashf,
            all_=False,
            to_dict=True
        )

        if not isinstance(user, dict):
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Користувач відсутній в системі."
            )
        
        for key, value in user.items():
            setattr(self, key, value)

        return self

    async def delete_user(self):
        try:
            await self.async_delete_data(
                instance=authefication,
                exp=authefication.c.hashf == self.hashf
            )
        except Exception as e:
            logger.error(f"\nObject: {self.__class__.__name__}\n" /
                         f"func: {self.delete_user.__name__}\n" /
                         f"Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Невідома помилка під час запиту."
            )
        
        return True

    async def get_restaurant(self) -> Restaurant:
        user_rest = await self.async_get_where(
            instance=restaurant,
            exp=restaurant.c.hashf == self.hashf,
            all_=False,
            to_dict=True
        )

        if not isinstance(user_rest, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Заклад відстуній в системі."
            )
        
        return Restaurant(**user_rest)
    
    async def add_restaurant(self, **kwargs) -> Restaurant:
        kwargs.update(hashf=self.hashf)

        try:
            restaurant_data: dict = await self.async_insert_data(
                instance=restaurant,
                to_dict=True,
                **kwargs
            )
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED, 
                detail='Ресторан з таким користувачем вже інсує'
            )
        
        except Exception as e:
            logger.error(f"\nObject: {self.__class__.__name__}\n" /
                         f"func: {self.add_restaurant.__name__}\n" /
                         f"Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Невідома помилка під час виконання операції."
            )

        return Restaurant(**restaurant_data)

    def get_parse_data(self):
        return dict((key, value) for key, value in self.__iter__() if key not in {"hashf", "password"})

    def __iter__(self):
        return iter([(k, v) for k, v in self.__dict__.items() if not k.startswith("_")])