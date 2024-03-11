from ...database.db.models._async import async_db
from fastapi.exceptions import HTTPException
from ...database.tables import ingredients
from ...settings import logger
from fastapi import status


class Ingredient(async_db):
    id: int
    ingredient: str
    dish_id: int
    restaurant_id: int

    def __init__(self, **kwargs) -> None:
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

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
            logger.error(
                f"\nObject: {self.__class__.__name__}\n" /
                f"func: {self.delete_ingredient.__name__}\n" /
                f"Error: {e}"
            )
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Невідома помилка під час виконання операції"
            )

        return True

    def __iter__(self):
        return iter([
            (k, v) for k, v in self.__dict__.items() 
            if not k.startswith("_")
        ])