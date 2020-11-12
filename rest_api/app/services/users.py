import os

import grpc
from loguru import logger

from app.users_pb2_grpc import UsersStub

USERS_SRV_PORT = os.getenv("USERS_SRV_PORT", "50052")
USERS_SRV_HOST = os.getenv("USERS_SRV_HOST", "")
USERS_DSN = f"{USERS_SRV_HOST}:{USERS_SRV_PORT}"


def get_users_service():
    logger.info(f"Users service at {USERS_DSN}")
    with grpc.insecure_channel(USERS_DSN) as channel:
        stub = UsersStub(channel)
        yield stub
