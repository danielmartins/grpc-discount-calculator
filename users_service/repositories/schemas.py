from datetime import datetime, date, timezone
from typing import Optional

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import BaseModel


class UserBase(BaseModel):
    id: Optional[str]
    first_name: str
    last_name: str
    date_of_birth: date


class UserCreate(UserBase):
    pass


class User(UserBase):
    class Config:
        orm_mode = True

    def dict(self, *args, **kwargs):
        as_dict = super().dict(*args, **kwargs)
        if "date_of_birth" in as_dict:
            original = as_dict["date_of_birth"]
            birthday = Timestamp()
            year, month, day = original.year, original.month, original.day
            birthday.FromDatetime(datetime(year, month, day))
            as_dict["date_of_birth"] = birthday
        return as_dict
