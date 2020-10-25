# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import discount_pb2 as discount__pb2


class DiscounterStub(object):
    """The Discount service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.calculate_discount = channel.unary_unary(
                '/discount.Discounter/calculate_discount',
                request_serializer=discount__pb2.DiscountRequest.SerializeToString,
                response_deserializer=discount__pb2.DiscountResponse.FromString,
                )


class DiscounterServicer(object):
    """The Discount service definition.
    """

    def calculate_discount(self, request, context):
        """Calculate discount by product
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DiscounterServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'calculate_discount': grpc.unary_unary_rpc_method_handler(
                    servicer.calculate_discount,
                    request_deserializer=discount__pb2.DiscountRequest.FromString,
                    response_serializer=discount__pb2.DiscountResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'discount.Discounter', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Discounter(object):
    """The Discount service definition.
    """

    @staticmethod
    def calculate_discount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/discount.Discounter/calculate_discount',
            discount__pb2.DiscountRequest.SerializeToString,
            discount__pb2.DiscountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
