from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    name: str
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, ge=0)


