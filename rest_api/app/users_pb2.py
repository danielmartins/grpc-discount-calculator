# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: users.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import messages_pb2 as messages__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='users.proto',
  package='users',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0busers.proto\x12\x05users\x1a\x0emessages.proto2l\n\x05Users\x12/\n\x08get_user\x12\x0f.GetUserRequest\x1a\x10.GetUserResponse\"\x00\x12\x32\n\tget_users\x12\x10.GetUsersRequest\x1a\x11.GetUsersResponse\"\x00\x62\x06proto3'
  ,
  dependencies=[messages__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_USERS = _descriptor.ServiceDescriptor(
  name='Users',
  full_name='users.Users',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=38,
  serialized_end=146,
  methods=[
  _descriptor.MethodDescriptor(
    name='get_user',
    full_name='users.Users.get_user',
    index=0,
    containing_service=None,
    input_type=messages__pb2._GETUSERREQUEST,
    output_type=messages__pb2._GETUSERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_users',
    full_name='users.Users.get_users',
    index=1,
    containing_service=None,
    input_type=messages__pb2._GETUSERSREQUEST,
    output_type=messages__pb2._GETUSERSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_USERS)

DESCRIPTOR.services_by_name['Users'] = _USERS

# @@protoc_insertion_point(module_scope)