from ....database.tables import authefication
from fastapi import HTTPException, status
from .restaurant import PersonRestaurant
from ..exc import exc


class Person(
    PersonRestaurant,
    exc
):

    id: int
    hashf: str
    email: str
    password: str
 
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