from datetime import datetime, timezone

import pytest
from google.protobuf.timestamp_pb2 import Timestamp

from ..app import messages_pb2


@pytest.fixture
def user():
    birthday = Timestamp()
    birthday.FromDatetime(datetime(1986, 2, 27, tzinfo=timezone.utc))
    usr_params = {
        "id": "123qweasd",
        "first_name": "daniel",
        "last_name": "santos",
        "date_of_birth": birthday,
    }
    return messages_pb2.User(**usr_params)


@pytest.fixture
def user_with_birthday_at_black_fridays():
    birthday = Timestamp()
    birthday.FromDatetime(datetime(1986, 11, 25, tzinfo=timezone.utc))
    usr_params = {
        "id": "123qweasd",
        "first_name": "daniel",
        "last_name": "santos",
        "date_of_birth": birthday,
    }
    return messages_pb2.User(**usr_params)


@pytest.fixture
def user_at_birthday(user, freezer):
    freezer.move_to("2020-02-27")
    return user


@pytest.fixture
def user_at_birthday(user, freezer):
    freezer.move_to("2020-02-27")
    return user


@pytest.fixture
def user_out_of_birthday(user, freezer):
    freezer.move_to("2020-03-27")
    return user


@pytest.fixture
def product_with_price_100():
    prd_params = {
        "id": "123qwe",
        "price_in_cents": 100,
        "title": "product a",
        "description": "description",
    }
    return messages_pb2.Product(**prd_params)
