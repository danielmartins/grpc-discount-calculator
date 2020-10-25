import logging

import grpc

from discount_service.discount_service import discount_pb2
from discount_service.discount_service import discount_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = discount_pb2_grpc.DiscounterStub(channel)
        response = stub.calculate_discount(discount_pb2.DiscountRequest(product_id='123', user_id='123aS'))
    print("Greeter client received: " + str(response))


if __name__ == '__main__':
    logging.basicConfig()
    run()
