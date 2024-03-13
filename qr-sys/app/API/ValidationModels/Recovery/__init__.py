from pydantic import BaseModel, Field, validator

from ....database.db.models.sync import sync_db
from ....database.tables import authefication
from ....framework import logger

from fastapi.exceptions import HTTPException


class ValidationEmail(BaseModel):
    email: str

class Recovery(ValidationEmail):
    code: str


class RecoveryPassword(BaseModel):
    id: int = Field(..., 
                    description="id користувача яке отримали після успішної перевірки коду")
    password: str = Field(..., description="Новий пароль для користувача")
