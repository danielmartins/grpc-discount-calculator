import logging

import grpc

from users_service.messages_pb2 import GetUserRequest
from users_service.users_pb2_grpc import UsersStub


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = UsersStub(channel)
        response = stub.get_user(GetUserRequest(user_id='49c55798-7c45-47cc-a133-a63b088a06b3'))
        print("Greeter client received: " + str(response))


if __name__ == '__main__':
    logging.basicConfig()
    run()
