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

    def __init__(self, **kwargs) -> None:
        super().__init__()

        kw_keys = set(kwargs.keys())
        obj_keys = set(self.__annotations__.keys())
        
        keys = obj_keys & kw_keys

        if any(keys) is False:
            raise Exception("Немає жодного атрибуту для " \
                            "ініціалізації користувача")

        for key in obj_keys & kw_keys:
            setattr(self, key, kwargs.get(key))

    
    async def initialize(self):
        search = []
        search.append(authefication.c.hashf == self.hashf) if self.hashf else None
        search.append(authefication.c.email == self.email) if self.email else None
        search.append(authefication.c.id == self.id) if self.id else None

        user: dict = await self.async_get_where(
            instance=authefication,
            and__=search,
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
    
    async def check_user(self):
        search = []
        search.append(authefication.c.email == self.email) if self.email else None
        search.append(authefication.c.hashf == self.hashf) if self.hashf else None

        if not search:
            raise Exception("Відсутні атрибути пошуку!")

        try:
            user: dict | None = await self.async_get_where(
                instance=authefication,
                and__=search,
                all_=False,
                to_dict=True
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.check_user.__name__,
                e=e
            )
        
        if isinstance(user, dict):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Користувач вже присутній в сисетмі!"
            )

    
    async def add_new_user(self):
        data = {k: getattr(self, k) for k in self.__annotations__.keys() if k != "id"}

        try:
            new_user: dict = await self.async_insert_data(
                instance=authefication,
                to_dict=True,
                **data
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.add_new_user.__name__,
                e=e
            )
        
        [setattr(self, k, v) for k, v in new_user.items()]
        return self

    async def update_user_data(self, **kwargs):
        if ("id" or "hashf") in kwargs.keys():
            raise Exception("Неможиво змінити унікальні" \
                            " ідентифікатори користувача!")
        
        try:
            new_data: dict = await self.async_update_data(
                instance=authefication,
                exp=authefication.c.hashf == self.hashf,
                to_dict=True,
                **kwargs
            )
        except Exception as e:
            raise self._throw_exeption_500(
                func=self.update_user_data.__name__,
                e=e
            )
        
        [setattr(self, key, value) for key, value in new_data.items()]
        return self

    async def delete_user(self):
        try:
            await self.async_delete_data(
                instance=authefication,
                exp=authefication.c.hashf == self.hashf
            )
        except Exception as e:
            raise self._throw_exeption_500(
                func=self.delete_user.__name__,
                e=e
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
            raise self._throw_exeption_500(
                func=self.add_restaurant.__name__,
                e=e
            )

        return Restaurant(**restaurant_data)

    def get_parse_data(self):
        return dict((key, value) for key, value in self.__iter__() if key not in {"hashf", "password"})
    
    def _throw_exeption_500(self, func, e: Exception):
        logger.error(f"\nObject: {self.__class__.__name__}\n" \
                         f"func: {func}" \
                         f"Error: {e}")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Невідома помилка під час транзакції"
        )

    def __iter__(self):
        return iter([(k, getattr(self, k)) for k, _ in self.__annotations__.items()])
    
    def __getattr__(self, item):
        if item in self.__annotations__.keys():
            self.__dict__[item] = None
        else:
            raise Exception("Не можливо додати новий атрибут!")