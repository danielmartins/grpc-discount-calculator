from typing import List

from app.messages_pb2 import GetUsersResponse
from . import schemas
from .discounter_pb2_grpc import DiscounterStub
from .messages_pb2 import GetProductsRequest, GetUserRequest, DiscountRequest, GetProductsResponse, GetUserResponse, \
    DiscountResponse, GetUsersRequest
from .products_pb2_grpc import ProductsStub
from .users_pb2_grpc import UsersStub


def get_products(service: ProductsStub) -> List[schemas.Product]:
    resp = service.get_products(GetProductsRequest())  # type: GetProductsResponse
    return [schemas.Product.from_orm(p) for p in resp.products]


def get_user(service: UsersStub, user_id: str) -> schemas.User:
    resp = service.get_user(GetUserRequest(user_id=user_id))  # type: GetUserResponse
    return schemas.User.from_orm(resp.user)


def get_users(service: UsersStub) -> List[schemas.User]:
    resp = service.get_users(GetUsersRequest())  # type: GetUsersResponse
    return [schemas.User.from_orm(u) for u in resp.users]


def calculate_discount(service: DiscounterStub, product: schemas.Product, user: schemas.User) -> schemas.Product:
    req = DiscountRequest(product_id=product.id, user_id=user.id)
    resp = service.calculate_discount(req)  # type: DiscountResponse
    if resp.discounted_price_in_cents:
        product.price_in_cents = resp.discounted_price_in_cents
    return product
