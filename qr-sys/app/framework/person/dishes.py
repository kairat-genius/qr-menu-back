from ...database.tables import ingredients, dishes
from fastapi.exceptions import HTTPException
from .ingredients import Ingredient
from typing import ByteString
from .exc import exc


class Dish(exc):
    id: int
    img: ByteString | None
    name: str
    price: int
    weight: int
    comment: str
    category_id: int
    restaurant_id: int

    async def get_ingredients(self) -> list[Ingredient]:
        ingredient = await self.async_get_where(
            instance=ingredients,
            and__=(
                ingredients.c.dish_id == self.id,
                ingredients.c.restaurant_id == self.restaurant_id
            ),
            to_object=Ingredient,
            to_dict=True
        )

        return ingredient
    
    async def add_ingredient(self, **kwargs):
        kwargs.update(
            dish_id=self.id,
            restaurant_id=self.restaurant_id
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
    
    async def delete_ingredient(self, ingredient_id: int) -> bool | HTTPException:
        try:
            await self.async_delete_data(
                instance=ingredients,
                and__=(
                    ingredients.c.id == ingredient_id,
                    ingredients.c.dish_id == self.id,
                    ingredients.c.restaurant_id == self.restaurant_id
                )
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.delete_ingredient.__name__,
                e=e
            )

        return True

    async def delete_dish(self):
        try:
            await self.async_delete_data(
                instance=dishes,
                and__=(
                    dishes.c.id == self.id,
                    dishes.c.category_id == self.category_id,
                    dishes.c.restaurant_id == self.restaurant_id
                )
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.delete_dish.__name__,
                e=e
            )

        return True