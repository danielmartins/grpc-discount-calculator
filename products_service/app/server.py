import logging
import os
from concurrent import futures

import grpc
from loguru import logger

from app import products_pb2_grpc, messages_pb2
from app.repositories import create_database, get_products, SessionLocal, Product


SRV_PORT = os.getenv("PRODUCTS_SRV_PORT", "50052")

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
    server_addrs = f"0.0.0.0:{SRV_PORT}"
    logger.info(f"Starting server at {server_addrs}")
    server.add_insecure_port(server_addrs)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
