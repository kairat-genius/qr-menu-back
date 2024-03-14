from .ingredient import RestaurantIngredient
from ....database.tables import restaurant
from fastapi import HTTPException, status
from .category import RestaurantCategory
from .dish import RestaurantDish
from typing import ByteString
from ..exc import exc



class Restaurant(
    RestaurantIngredient,
    RestaurantCategory,
    RestaurantDish,
    exc
):

    id: int
    name: str
    address: str | None
    start_day: str | None
    end_day: str | None
    start_time: str | None
    end_time: str | None
    logo: ByteString | None

    async def initialize(self):
        try:
            restaurant_data: dict = await self.async_get_where(
                instance=restaurant,
                and__=(
                    restaurant.c.id == self.id,
                    restaurant.c.name == self.name
                ),
                to_dict=True,
                all_=False
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.initialize.__name__,
                e=e
            )
        
        if not isinstance(restaurant_data, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Відсутній заклад."
            )
        
        self.update_attr(**restaurant_data)
        return self

    async def get_full_data(self, id: bool = False):
        category = await self.get_categories()

        result = {
            **self.get_parse_data(id=id),
            "categories": [
                {**i.get_parse_data(id=id), 
                    "dishes": [
                        {**j.get_parse_data(id=id),
                            "ingredients": [
                                l.get_parse_data(id=id) for l in await j.get_ingredients()
                            ] 
                        } for j in await i.get_dishes()
                    ]
                } for i in category 
            ]
        }

        return result
    
    async def update_restaurant(self):
        try:
            new_data: dict = await self.async_update_data(
                instance=restaurant,
                exp=restaurant.c.id == self.id,
                to_dict=True,
                **self.get_parse_data(id=True)
            )        
        except Exception as e:
            raise self._throw_exeption_500(
                func=self.update_restaurant.__name__,
                e=e
            )
        
        if not isinstance(new_data, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Відсутній заклад."
            )
        
        self.update_attr(**new_data)
        return self
    
    async def delete_restaurant(self):
        try:
            await self.async_delete_data(
                instance=restaurant,
                exp=restaurant.c.id == self.id
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.delete_restaurant.__name__,
                e=e
            )
    
    async def delete_data(self, *args):
        data = {k: None for k in args}

        try:
            new_data: dict = await self.async_update_data(
                    instance=restaurant,
                    exp=restaurant.c.id == self.id,
                    to_dict=True,
                    **data
                )  
        except Exception as e:
            raise self._throw_exeption_500(
                func=self.delete_data.__name__,
                e=e
            )
        
        if not isinstance(new_data, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Відсутній заклад."
            )

        self.update_attr(**new_data)
        return self