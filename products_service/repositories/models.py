import uuid

from sqlalchemy import Column, String, Integer

from .database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True, unique=True, nullable=False, default=generate_uuid)
    price_in_cents = Column(Integer, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
