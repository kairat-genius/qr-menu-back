from ....database.tables import categories
from fastapi import HTTPException, status
from ..categories import Category


class RestaurantCategory:

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