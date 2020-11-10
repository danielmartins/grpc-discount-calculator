# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import messages_pb2 as messages__pb2


class UsersStub(object):
    """The User service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_user = channel.unary_unary(
                '/users.Users/get_user',
                request_serializer=messages__pb2.GetUserRequest.SerializeToString,
                response_deserializer=messages__pb2.GetUserResponse.FromString,
                )


class UsersServicer(object):
    """The User service definition.
    """

    def get_user(self, request, context):
        """Get User By ID
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UsersServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_user': grpc.unary_unary_rpc_method_handler(
                    servicer.get_user,
                    request_deserializer=messages__pb2.GetUserRequest.FromString,
                    response_serializer=messages__pb2.GetUserResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'users.Users', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Users(object):
    """The User service definition.
    """

    @staticmethod
    def get_user(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/users.Users/get_user',
            messages__pb2.GetUserRequest.SerializeToString,
            messages__pb2.GetUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
