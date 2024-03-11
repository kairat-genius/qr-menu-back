from ...database.db.models._async import async_db
from ...database.tables import dishes, categories
from fastapi.exceptions import HTTPException
from ...settings import logger
from fastapi import status
from .dishes import Dish


class Category(async_db):
    id: int
    category: str
    color: list[int]
    restaurant_id: int

    def __init__(self, **kwargs) -> None:
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)
    
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
            raise self._throw_exception_500(
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
            raise self._throw_exception_500(
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
            raise self._throw_exception_500(
                func=self.delete_category.__name__,
                e=e
            )

        return True
    
    def _throw_exception_500(self, func: str, e: str):
        logger.error(
                f"\nObject: {self.__class__.__name__}\n" /
                f"func: {func}\n" /
                f"Error: {e}"
            )
            
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Невідома помилка під час виконання операції"
        )

    def __iter__(self):
        return iter([(k, v) for k, v in self.__dict__.items() if not k.startswith("_")])