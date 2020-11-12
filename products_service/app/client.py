import logging

import grpc

from app import products_pb2_grpc, messages_pb2


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = products_pb2_grpc.ProductsStub(channel)
        response = stub.get_product(messages_pb2.GetProductRequest(product_id='123'))
        print("Greeter client received: " + str(response))
        response = stub.get_products(messages_pb2.GetProductsRequest())
        print("Greeter client received: " + str(response))


if __name__ == '__main__':
    logging.basicConfig()
    run()
