import os
from typing import List

import grpc
from fastapi import FastAPI, Depends
from loguru import logger

from . import repositories, schemas
from .discounter_pb2_grpc import DiscounterStub
from .products_pb2_grpc import ProductsStub
from .users_pb2_grpc import UsersStub

app = FastAPI()

USERS_SRV_PORT = os.getenv("USERS_SRV_PORT", "50052")
USERS_SRV_HOST = os.getenv("USERS_SRV_HOST", "")

PRODUCTS_SRV_HOST = os.getenv("PRODUCTS_SRV_HOST", "")
PRODUCTS_SRV_PORT = os.getenv("PRODUCTS_SRV_PORT", "")

DISCOUNT_SRV_HOST = os.getenv("DISCOUNT_SRV_HOST", "")
DISCOUNT_SRV_PORT = os.getenv("DISCOUNT_SRV_PORT", "")

USERS_DSN = f"{USERS_SRV_HOST}:{USERS_SRV_PORT}"
PRODUCTS_DSN = f"{PRODUCTS_SRV_HOST}:{PRODUCTS_SRV_PORT}"
DISCOUNT_DSN = f"{DISCOUNT_SRV_HOST}:{DISCOUNT_SRV_PORT}"


def get_users_service():
    logger.info(f"Users service at {USERS_DSN}")
    with grpc.insecure_channel(USERS_DSN) as channel:
        stub = UsersStub(channel)
        yield stub


def get_products_service():
    logger.info(f"Products service at {PRODUCTS_DSN}")
    with grpc.insecure_channel(PRODUCTS_DSN) as channel:
        stub = ProductsStub(channel)
        yield stub


def get_discount_service():
    logger.info(f"Discount service at {DISCOUNT_DSN}")
    with grpc.insecure_channel(DISCOUNT_DSN) as channel:
        stub = DiscounterStub(channel)
        yield stub


@app.get("/products/", response_model=List[schemas.Product])
def get_products(db: ProductsStub = Depends(get_products_service)):
    products = repositories.get_products(db)
    return products


@app.get("/products/{user_id}/", response_model=List[schemas.Product])
def get_products(user_id: str, products_srv: ProductsStub = Depends(get_products_service),
                 discount_srv: DiscounterStub = Depends(get_discount_service),
                 users_srv: UsersStub = Depends(get_users_service)):
    user = repositories.get_user(users_srv, user_id)
    products = repositories.get_products(products_srv)
    products = [repositories.calculate_discount(discount_srv, p, user) for p in products]
    return products


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: str, db: UsersStub = Depends(get_users_service)):
    return repositories.get_user(db, user_id)


@app.get("/users/", response_model=List[schemas.User])
def get_users(users_srv: UsersStub = Depends(get_users_service)):
    return repositories.get_users(users_srv)
