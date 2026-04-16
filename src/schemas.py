from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)

