from ....database.tables import restaurant
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from ..restaurant import Restaurant


class PersonRestaurant:

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