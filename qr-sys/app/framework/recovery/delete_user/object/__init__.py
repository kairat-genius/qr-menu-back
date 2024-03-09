from .....settings import REDIS_DB, DELETE_USER_TIME
from ...password.object import recovery_codes
from ....redis import get_redis_connection
from typing import Any
import os


code = get_redis_connection(int(os.environ.get("REDIS_DB", REDIS_DB)) + 4)

class delete_user_codes(recovery_codes):

    def __setitem__(self, key: Any, value: Any) -> None:
        code.set(key, value)
        code.expire(key, DELETE_USER_TIME)

    def __delitem__(self, key: Any) -> None:
        code.delete(key)

    def __getitem__(self, key: Any) -> Any:
        return code.get(key)