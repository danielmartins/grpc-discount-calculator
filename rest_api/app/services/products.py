import os

import grpc
from loguru import logger

from app.products_pb2_grpc import ProductsStub

PRODUCTS_SRV_HOST = os.getenv("PRODUCTS_SRV_HOST", "")
PRODUCTS_SRV_PORT = os.getenv("PRODUCTS_SRV_PORT", "")
PRODUCTS_DSN = f"{PRODUCTS_SRV_HOST}:{PRODUCTS_SRV_PORT}"


def get_products_service():
    logger.info(f"Products service at {PRODUCTS_DSN}")
    with grpc.insecure_channel(PRODUCTS_DSN) as channel:
        stub = ProductsStub(channel)
        yield stub
