from ...database.tables import dishes, categories
from fastapi.exceptions import HTTPException
from .dishes import Dish
from .exc import exc


class Category(exc):
    id: int
    category: str
    color: list[int]
    restaurant_id: int

    async def get_dishes(self) -> list[Dish]:
        dish = await self.async_get_where(
            instance=dishes,
            and__=(
                dishes.c.restaurant_id == self.restaurant_id,
                dishes.c.category_id == self.id
            ),
            to_dict=True,
            to_object=Dish
        )

        return dish
    
    async def add_dish(self, **kwargs) -> Dish:
        kwargs.update(
            restaurant_id=self.restaurant_id,
            category_id=self.id
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
    
    async def delete_dish(self, dish_id: int) -> bool | HTTPException:
        try:
            await self.async_delete_data(
                instance=dishes,
                and__=(
                    dishes.c.category_id == self.id,
                    dishes.c.restaurant_id == self.restaurant_id,
                    dishes.c.id == dish_id
                )
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.delete_category.__name__,
                e=e
            )
        
        return True

    async def delete_category(self) -> bool | HTTPException:
        try:
            await self.async_delete_data(
                instance=categories,
                and__=(
                    categories.c.id == self.id,
                    categories.c.restaurant_id == self.restaurant_id
                )
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.delete_category.__name__,
                e=e
            )

        return True
