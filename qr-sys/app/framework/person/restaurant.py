from ...database.tables import (categories, restaurant,
                                 dishes, ingredients)
from ...database.db.models._async import async_db
from fastapi.exceptions import HTTPException
from .ingredients import Ingredient
from .categories import Category
from ...settings import logger
from typing import ByteString
from fastapi import status
from .dishes import Dish


class Restaurant(async_db):
    id: int
    name: str
    address: str | None
    start_day: str | None
    end_day: str | None
    start_time: str | None
    end_time: str | None
    logo: ByteString | None

    def __init__(self, **kwargs) -> None:
        super().__init__()
        [
            setattr(self, key, value) 
            for key, value in kwargs.items() 
            if key != "hashf"
        ]

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
    
    async def update_restaurant(self):
        try:
            new_data: dict = await self.async_update_data(
                instance=restaurant,
                exp=restaurant.c.id == self.id,
                to_dict=True,
                **self.get_filter_data()
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

    async def get_categories(self) -> list[Category]:
        categ = await self.async_get_where(
            instance=categories,
            exp=categories.c.restaurant_id == self.id,
            to_object=Category,
            to_dict=True
        )

        return categ
    
    async def get_category(self, category_id: int) -> Category:
        categ = await self.async_get_where(
            instance=categories,
            and__=(
                categories.c.restaurant_id == self.id,
                categories.c.id == category_id
            ),
            to_dict=True,
            all_=False,
        )

        if not isinstance(categ, dict):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Не знайдено жодної категорії з id: {category_id}"
            )
        
        return Category(**categ)
    
    async def add_category(self, **kwargs) -> Category:
        kwargs.update(restaurant_id=self.id)

        try:
            categ = await self.async_insert_data(
                instance=categories,
                to_dict=True,
                **kwargs
            )
        except Exception as e:
            raise self._throw_exeption_500(
                func=self.add_category.__name__,
                e=e
            )

        return Category(**categ)
    
    async def delete_category(self, type: str = "category", id: int = None):
        and__ = [categories.c.restaurant_id == self.id]
        and__.append(categories.c.id == id) if type == "category" else None

        try:
            await self.async_delete_data(
                instance=categories,
                and__=tuple(and__)
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.delete_category.__name__,
                e=e
            )

        return "Категорія видалена успішно!" if type == "category" else "Всі категорії були видаленні!" 
    

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
    
    async def add_ingredient(self, **kwargs):
        kwargs.update(
            restaurant_id=self.id
        )

        try:
            new_ingredient = await self.async_insert_data(
                instance=ingredients,
                to_dict=True,
                **kwargs
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.add_ingredient.__name__,
                e=e
            )
        
        return Ingredient(**new_ingredient)
    

    async def delete_ingredient(self, ingredient_id: int, dish_id: int) -> bool | HTTPException:
        try:
            await self.async_delete_data(
                instance=ingredients,
                and__=(
                    ingredients.c.id == ingredient_id,
                    ingredients.c.dish_id == dish_id,
                    ingredients.c.restaurant_id == self.id
                )
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.delete_ingredient.__name__,
                e=e
            )

        return True
    
    async def get_ingredients(self, dish_id: int) -> list[Ingredient]:
        ingredient = await self.async_get_where(
            instance=ingredients,
            and__=(
                ingredients.c.dish_id == dish_id,
                ingredients.c.restaurant_id == self.id
            ),
            to_object=Ingredient,
            to_dict=True
        )

        return ingredient

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

    def get_filter_data(self):
        return {k: v for k, v in dict(self).items() if k != "id"}

    def update_attr(self, **kwargs):
        for key, value in kwargs.items():
            if key not in ("hashf", "id"):
                setattr(self, key, value)

    def _throw_exeption_500(self, func, e: Exception):
        logger.error(f"\nObject: {self.__class__.__name__}\n" \
                         f"func: {func}" \
                         f"Error: {e}")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Невідома помилка під час транзакції"
        )
    
    def __iter__(self):
        return iter([(k, v) for k, v in self.__dict__.items() if not k.startswith("_")])