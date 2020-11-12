import os
from concurrent import futures

import grpc
from loguru import logger

from app.messages_pb2 import (
    GetUserRequest,
    GetUserResponse,
    User as ServiceUser,
    GetUsersRequest,
    GetUsersResponse,
)
from app.repositories import create_database, SessionLocal, get_user, User, get_users
from app.users_pb2_grpc import UsersServicer, add_UsersServicer_to_server


SRV_PORT = os.getenv("USERS_SRV_PORT", "50052")

create_database()
db = SessionLocal()


class Users(UsersServicer):
    def _build_user(self, orm_object, schema_cls):
        user = schema_cls.from_orm(orm_object)
        return ServiceUser(**user.dict())

    def get_user(self, request: GetUserRequest, context):
        logger.info(f"get user {request.user_id}")
        user = self._build_user(get_user(db, request.user_id), User) or None
        return GetUserResponse(user=user)

    def get_users(self, request: GetUsersRequest, context):
        logger.info(f"get users")
        users = [self._build_user(u, User) for u in get_users(db)]
        return GetUsersResponse(users=users)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UsersServicer_to_server(Users(), server)
    server_addrs = f"0.0.0.0:{SRV_PORT}"
    logger.info(f"Starting server at {server_addrs}")
    server.add_insecure_port(server_addrs)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
