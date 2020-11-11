from typing import List

import grpc
from fastapi import FastAPI, Depends

from . import repositories, schemas
from .discounter_pb2_grpc import DiscounterStub
from .products_pb2_grpc import ProductsStub
from .users_pb2_grpc import UsersStub

app = FastAPI()


def get_users_service():
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = UsersStub(channel)
        yield stub


def get_products_service():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ProductsStub(channel)
        yield stub


def get_discount_service():
    with grpc.insecure_channel('localhost:50053') as channel:
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
def get_user(user_id: str, db: UsersStub = Depends(get_users_service)):
    return repositories.get_user(db, user_id)
