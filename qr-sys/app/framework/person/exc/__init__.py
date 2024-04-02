from ....database.db.models._async import async_db
from fastapi import HTTPException, status
from ....settings import logger


class exc(async_db):
    
    def __init__(self, **kwargs) -> None:
        kw_keys = set(kwargs.keys())
        obj_keys = set(self.__annotations__.keys())
        
        keys = obj_keys & kw_keys

        if any(keys) is False:
            raise Exception("Немає жодного атрибуту для " \
                            "ініціалізації користувача")

        for key in obj_keys & kw_keys:
            setattr(self, key, kwargs.get(key))

    def get_parse_data(
            self, 
            id: bool = False,
            secrets: bool = False
        ):
        data = self.get_data()

        if id:
            data = {k: v for k, v in data.items()
                    if not k.endswith("id")}

        if secrets:
            data = {k: v for k, v in data.items()
                    if k not in ("hashf", "password")}

        return data

    def get_data(self):
        return self.__dict__

    def _throw_exeption_500(self, func, e: Exception):
        logger.error(f"\nObject: {self.__class__.__name__}\n" \
                         f"func: {func}" \
                         f"Error: {e}")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Невідома помилка під час транзакції"
        )
    
    def __getattr__(self, item):
        if item in self.__annotations__.keys():
            self.__dict__[item] = None
        else:
            raise Exception("Не можливо додати новий атрибут!")
    
    def update_attr(self, **kwargs):
        for key, value in kwargs.items():
            if key not in ("hashf", "id"):
                setattr(self, key, value)