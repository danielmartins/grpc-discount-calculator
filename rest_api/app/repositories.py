from typing import List, Optional

from loguru import logger

from . import schemas
from .discounter_pb2_grpc import DiscounterStub
from .messages_pb2 import (
    GetProductsRequest,
    GetUserRequest,
    DiscountRequest,
    GetProductsResponse,
    GetUserResponse,
    DiscountResponse,
    GetUsersRequest,
    GetProductRequest,
    GetProductResponse,
    GetUsersResponse,
)
from .products_pb2_grpc import ProductsStub
from .users_pb2_grpc import UsersStub


def get_products(service: ProductsStub) -> List[schemas.Product]:
    try:
        resp = service.get_products(GetProductsRequest())  # type: GetProductsResponse
        return [schemas.Product.from_orm(p) for p in resp.products]
    except Exception:
        logger.exception("Can't retrieve products")


def get_product(service: ProductsStub, product_id: str) -> Optional[schemas.Product]:
    try:
        resp = service.get_product(
            GetProductRequest(product_id=product_id)
        )  # type: GetProductResponse
        return schemas.Product.from_orm(resp.product)
    except Exception:
        logger.exception("Can't retrieve product")


def get_user(service: UsersStub, user_id: str) -> Optional[schemas.User]:
    try:
        resp = service.get_user(
            GetUserRequest(user_id=user_id)
        )  # type: GetUserResponse
        return schemas.User.from_orm(resp.user)
    except Exception:
        logger.exception("Can't retrieve user")


def get_users(service: UsersStub) -> List[schemas.User]:
    try:
        resp = service.get_users(GetUsersRequest())  # type: GetUsersResponse
        return [schemas.User.from_orm(u) for u in resp.users]
    except Exception:
        logger.exception("Can't retrieve users")


def calculate_discount(
    service: DiscounterStub, product: schemas.Product, user: schemas.User
) -> schemas.Product:
    try:
        req = DiscountRequest(product_id=product.id, user_id=user.id)
        resp = service.calculate_discount(req)  # type: DiscountResponse
        if resp.discounted_price_in_cents:
            product.price_in_cents = resp.discounted_price_in_cents
        return product
    except Exception:
        logger.exception("Can't calculate discount")
    finally:
        return product
