from ....database.tables import ingredients
from ..ingredients import Ingredient
from fastapi import HTTPException


class RestaurantIngredient:

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