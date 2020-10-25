import logging
from concurrent import futures

import grpc

from discount_service.discount_service import discount_pb2_grpc, discount_pb2

logger = logging.getLogger(__name__)


class Discounter(discount_pb2_grpc.DiscounterServicer):
    def calculate_discount(self, request, context):
        logger.info("Calculating discount")
        params = {"product_id": "123", "full_price_in_cents": 123456, "discounted_price_in_cents": 12344}
        return discount_pb2.DiscountResponse(**params)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    discount_pb2_grpc.add_DiscounterServicer_to_server(Discounter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
