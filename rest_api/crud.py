from typing import List

from messages_pb2 import GetUserRequest
from .messages_pb2 import GetProductsRequest
from .products_pb2_grpc import ProductsStub
from .schemas import Product, User
from .users_pb2_grpc import UsersStub


def get_products(service: ProductsStub) -> List[Product]:
    resp = service.get_products(GetProductsRequest())
    return [Product.from_orm(p) for p in resp.products]


def get_user(service: UsersStub, user_id) -> User:
    resp = service.get_user(GetUserRequest(user_id=user_id))
    return User.from_orm(resp.user)
