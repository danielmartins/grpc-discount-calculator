import logging
from concurrent import futures

import grpc

from . import discounter_pb2
from . import discounter_pb2_grpc

logger = logging.getLogger(__name__)


class Discounter(discounter_pb2_grpc.DiscounterServicer):
    def calculate_discount(self, request, context):
        logger.info("Calculating discount")
        params = {"product_id": "123", "full_price_in_cents": 123456, "discounted_price_in_cents": 12344}
        return discounter_pb2.DiscountResponse(**params)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    discounter_pb2_grpc.add_DiscounterServicer_to_server(Discounter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()