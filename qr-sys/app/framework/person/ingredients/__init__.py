from ....database.tables import ingredients
from ..exc import exc


class Ingredient(exc):
    id: int
    ingredient: str
    dish_id: int
    restaurant_id: int

    async def delete_ingredient(self):
        try:
            await self.async_delete_data(
                instance=ingredients,
                and__=(
                    ingredients.c.id == self.id,
                    ingredients.c.dish_id == self.dish_id,
                    ingredients.c.restaurant_id == self.restaurant_id
                )
            )

        except Exception as e:
            raise self._throw_exeption_500(
                func=self.delete_ingredient.__name__,
                e=e
            )

        return True