import logging
from concurrent import futures

import grpc

from products_service import products_pb2_grpc, messages_pb2
from products_service.repositories import create_database, get_products, SessionLocal, Product

logger = logging.getLogger(__name__)

create_database()
db = SessionLocal()


class Products(products_pb2_grpc.ProductsServicer):
    def _get_products(self):
        products = [Product.from_orm(p) for p in get_products(db)]
        return [messages_pb2.Product(**p.dict()) for p in products]

    def get_product(self, request, context):
        logger.info("Getting one product")
        products = self._get_products()
        return messages_pb2.GetProductResponse(product=products[0] if products else None)

    def get_products(self, request, context):
        logger.info("Getting all products")
        products = self._get_products()
        return messages_pb2.GetProductsResponse(products=products)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    products_pb2_grpc.add_ProductsServicer_to_server(Products(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
