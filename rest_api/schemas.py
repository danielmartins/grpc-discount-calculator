from datetime import date
from typing import Optional

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic.main import BaseModel


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


class ProtoBufTimestamp(date):

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, Timestamp):
            return v.ToDatetime().date()
        return v

    def __repr__(self):
        return f'Timestamp({super().__repr__()})'


class UserBase(BaseModel):
    id: Optional[str]
    first_name: str
    last_name: str
    date_of_birth: ProtoBufTimestamp


class UserCreate(UserBase):
    pass


class User(UserBase):
    pass

    class Config:
        orm_mode = True
