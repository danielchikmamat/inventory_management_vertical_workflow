from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, ge=0)



class ItemFilter(BaseModel):
    threshold: Optional[int] = Field(default=None, ge=0)
    min_price: Optional[float] = Field(default=None, ge=0)
    max_price: Optional[float] = Field(default=None, ge=0)
    # add more filters here as needed
