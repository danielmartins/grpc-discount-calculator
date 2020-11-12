import json

from faker import Faker
from invoke import task
from loguru import logger
from sqlalchemy.exc import IntegrityError

from app.repositories import UserCreate, create_user, create_database, SessionLocal


create_database()
fake = Faker()
db = SessionLocal()


@task
def generate_fake(ctx, qty=100):
    logger.info(f"Generating {qty} fake products")
    for i in range(qty):
        user = UserCreate(first_name=fake.first_name(),
                          last_name=fake.last_name(),
                          date_of_birth=fake.date_of_birth())
        create_user(db, user)
        logger.info(f"User - {user.first_name} created")


@task
def load_fixture(ctx, name):
    logger.info(f"Loading fixture {name}")
    with open(f"fixtures/{name}.json") as fixture:
        products = json.load(fixture)
        for p in products:
            user = UserCreate(**p)
            try:
                create_user(db, user)
                logger.info(f"User - {user.first_name} created")
            except IntegrityError:
                logger.warning(f"User with id '{user.id}' already exists")
