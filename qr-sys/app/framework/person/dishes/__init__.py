from ....database.tables import dishes
from .ingredient import DishIngredient
from typing import ByteString
from ..exc import exc


class Dish(
    DishIngredient,
    exc
):
    
    id: int
    img: ByteString | None
    name: str
    price: int
    weight: int
    comment: str
    category_id: int
    restaurant_id: int

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