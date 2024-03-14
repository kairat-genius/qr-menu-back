from ....database.tables  import dishes
from fastapi import HTTPException
from ..dishes import Dish


class RestaurantDish:

    async def add_dish(self, **kwargs) -> Dish:
        kwargs.update(
            restaurant_id=self.id
        )

        try:
            new_dish = await self.async_insert_data(
                instance=dishes,
                to_dict=True,
                **kwargs
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.add_dish.__name__,
                e=e
            )
        
        return Dish(**new_dish)

    async def get_dishes(self, category_id: int) -> list[Dish]:
        dish = await self.async_get_where(
            instance=dishes,
            and__=(
                dishes.c.restaurant_id == self.id,
                dishes.c.category_id == category_id
            ),
            to_dict=True,
            to_object=Dish
        )

        return dish
    
    async def delete_dish(self, category_id: int, dish_id: int) -> bool | HTTPException:
        try:
            await self.async_delete_data(
                instance=dishes,
                and__=(
                    dishes.c.category_id == category_id,
                    dishes.c.restaurant_id == self.id,
                    dishes.c.id == dish_id
                )
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.delete_category.__name__,
                e=e
            )
        
        return True