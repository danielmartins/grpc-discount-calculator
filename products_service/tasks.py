import json

from faker import Faker
from invoke import task
from loguru import logger
from sqlalchemy.exc import IntegrityError

from app.repositories import create_product, SessionLocal, ProductCreate

fake = Faker()
db = SessionLocal()


@task
def generate_fake(ctx, qty=100):
    logger.info(f"Generating {qty} fake products")
    for i in range(qty):
        product = ProductCreate(title=fake.bs(), price_in_cents=fake.pyint(100, 100000))
        create_product(db, product)
        logger.info(f"Product - {product.title} created")


@task
def load_fixture(ctx, name):
    logger.info(f"Loading fixture {name}")
    with open(f"fixtures/{name}.json") as fixture:
        products = json.load(fixture)
        for p in products:
            product = ProductCreate(**p)
            try:
                create_product(db, product)
                logger.info(f"Product - {product.title} created")
            except IntegrityError:
                logger.warning(f"Product with id '{product.id}' already exists")
