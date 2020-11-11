import logging
from concurrent import futures

import grpc
from loguru import logger

from discount_service import discounter_pb2_grpc
from discount_service.messages_pb2 import GetProductRequest, GetUserRequest, DiscountResponse
from discount_service.products_pb2_grpc import ProductsStub
from discount_service.use_cases.discount import DiscountUseCase
from discount_service.users_pb2_grpc import UsersStub


def get_users_service():
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = UsersStub(channel)
        yield stub


def get_products_service():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ProductsStub(channel)
        yield stub


class Discounter(discounter_pb2_grpc.DiscounterServicer):
    def _get_product(self, product_id):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = ProductsStub(channel)
            resp = stub.get_product(GetProductRequest(product_id=product_id))
            return resp.product

    def _get_user(self, user_id):
        with grpc.insecure_channel('localhost:50052') as channel:
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
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
