from pydantic import BaseModel


class DeleteUser(BaseModel):
    code: str