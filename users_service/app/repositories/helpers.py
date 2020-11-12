from loguru import logger

from .database import Base, engine


def create_database():
    logger.debug("Creating database if needed")
    Base.metadata.create_all(bind=engine)
