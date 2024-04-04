from pydantic import Field
from ..Restaurant import RestaurantLogo


class EmailSupport(RestaurantLogo):
    theme: str = Field(..., description="Тема листа")
    body: str = Field(..., description="Тіло листа")