import logging
from concurrent import futures

import grpc

from users_service import messages_pb2, users_pb2_grpc
from users_service.messages_pb2 import GetUserRequest
from users_service.repositories import create_database, SessionLocal, get_user, User
from users_service.users_pb2_grpc import UsersServicer

logger = logging.getLogger(__name__)

create_database()
db = SessionLocal()


class Users(UsersServicer):
    def _build_user(self, orm_object, schema_cls):
        user = schema_cls.from_orm(orm_object)
        return messages_pb2.User(**user.dict())

    def get_user(self, request: GetUserRequest, context):
        logger.info(f"get user {request.user_id}")
        user = self._build_user(get_user(db, request.user_id), User) or None
        return messages_pb2.GetUserResponse(user=user)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UsersServicer_to_server(Users(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
