from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    id: Optional[str]
    title: str
    price_in_cents: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    description: Optional[str]

    class Config:
        orm_mode = True
