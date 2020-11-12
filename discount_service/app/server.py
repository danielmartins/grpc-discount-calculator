import logging
import os
from concurrent import futures

import grpc
from loguru import logger

from app import discounter_pb2_grpc
from app.messages_pb2 import GetProductRequest, GetUserRequest, DiscountResponse
from app.products_pb2_grpc import ProductsStub
from app.use_cases.discount import DiscountUseCase
from app.users_pb2_grpc import UsersStub

SRV_PORT = os.getenv("DISCOUNT_SRV_PORT", "50052")
USERS_SRV_PORT = os.getenv("USERS_SRV_PORT", "50052")
USERS_SRV_HOST = os.getenv("USERS_SRV_HOST", "")
PRODUCTS_SRV_HOST = os.getenv("PRODUCTS_SRV_HOST", "")
PRODUCTS_SRV_PORT = os.getenv("PRODUCTS_SRV_PORT", "")

USERS_DSN = f"{USERS_SRV_HOST}:{USERS_SRV_PORT}"
PRODUCTS_DSN = f"{PRODUCTS_SRV_HOST}:{PRODUCTS_SRV_PORT}"


def get_users_service():
    with grpc.insecure_channel(USERS_DSN) as channel:
        stub = UsersStub(channel)
        yield stub


def get_products_service():
    with grpc.insecure_channel(PRODUCTS_DSN) as channel:
        stub = ProductsStub(channel)
        yield stub


class Discounter(discounter_pb2_grpc.DiscounterServicer):
    def _get_product(self, product_id):
        with grpc.insecure_channel(PRODUCTS_DSN) as channel:
            stub = ProductsStub(channel)
            resp = stub.get_product(GetProductRequest(product_id=product_id))
            return resp.product

    def _get_user(self, user_id):
        with grpc.insecure_channel(USERS_DSN) as channel:
            stub = UsersStub(channel)
            resp = stub.get_user(GetUserRequest(user_id=user_id))
            return resp.user

    def calculate_discount(self, request, context):
        logger.info("Calculating discount")
        user = self._get_user(request.user_id)
        product = self._get_product(request.product_id)
        use_case = DiscountUseCase()
        price = use_case.calculate(product=product, user=user)

        params = {"product_id": product.id,
                  "full_price_in_cents": product.price_in_cents,
                  "discounted_price_in_cents": price}
        return DiscountResponse(**params)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    discounter_pb2_grpc.add_DiscounterServicer_to_server(Discounter(), server)
    server_addrs = f"0.0.0.0:{SRV_PORT}"
    logger.info(f"Starting server at {server_addrs}")
    server.add_insecure_port(server_addrs)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
