from typing import List

from fastapi import FastAPI, Depends
from loguru import logger

from . import repositories, schemas, services
from .discounter_pb2_grpc import DiscounterStub
from .products_pb2_grpc import ProductsStub
from .users_pb2_grpc import UsersStub

app = FastAPI()


@app.get("/products/", response_model=List[schemas.Product])
def get_products(db: ProductsStub = Depends(services.products)):
    products = repositories.get_products(db)
    return products


@app.get("/products/{user_id}/", response_model=List[schemas.Product])
def get_products_with_discount(user_id: str, products_srv: ProductsStub = Depends(services.products),
                               discount_srv: DiscounterStub = Depends(services.discount),
                               users_srv: UsersStub = Depends(services.users)):
    user = repositories.get_user(users_srv, user_id)
    products = repositories.get_products(products_srv)
    products = [repositories.calculate_discount(discount_srv, p, user) for p in products]
    return products


@app.get("/products/{user_id}/{product_id}/", response_model=schemas.Product)
def get_product_with_discount(user_id: str, product_id: str,
                              products_srv: ProductsStub = Depends(services.products),
                              discount_srv: DiscounterStub = Depends(services.discount),
                              users_srv: UsersStub = Depends(services.users)):
    user = repositories.get_user(users_srv, user_id)
    logger.info(f"User -> {user}")
    product = repositories.get_product(products_srv, product_id)
    logger.info(f"Product -> {product}")
    return repositories.calculate_discount(discount_srv, product, user)


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: str, db: UsersStub = Depends(services.users)):
    return repositories.get_user(db, user_id)


@app.get("/users/", response_model=List[schemas.User])
def get_users(users_srv: UsersStub = Depends(services.users)):
    return repositories.get_users(users_srv)
