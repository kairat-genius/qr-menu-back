from ....database.tables import categories
from fastapi import HTTPException
from .dish import CategoryDish
from ..exc import exc


class Category(
    CategoryDish,
    exc
):

    id: int
    category: str
    color: list[int]
    restaurant_id: int

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