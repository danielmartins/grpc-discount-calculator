import os

import grpc
from loguru import logger

from app.discounter_pb2_grpc import DiscounterStub

DISCOUNT_SRV_HOST = os.getenv("DISCOUNT_SRV_HOST", "")
DISCOUNT_SRV_PORT = os.getenv("DISCOUNT_SRV_PORT", "")

DISCOUNT_DSN = f"{DISCOUNT_SRV_HOST}:{DISCOUNT_SRV_PORT}"


def get_discount_service():
    logger.info(f"Discount service at {DISCOUNT_DSN}")
    with grpc.insecure_channel(DISCOUNT_DSN) as channel:
        stub = DiscounterStub(channel)
        yield stub
