from typing import List

import grpc
from fastapi import FastAPI, Depends

from . import crud, schemas
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


@app.get("/products/", response_model=List[schemas.Product])
def get_products(db: ProductsStub = Depends(get_products_service)):
    products = crud.get_products(db)
    return products


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: str, db: UsersStub = Depends(get_users_service)):
    return crud.get_user(db, user_id)
