# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: groupservice.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12groupservice.proto\"\"\n\x0emembersRequest\x12\x10\n\x08group_id\x18\x01 \x01(\t\"\x1f\n\x0cmembersReply\x12\x0f\n\x07message\x18\x01 \x01(\t2>\n\x0cGroupService\x12.\n\nGetMembers\x12\x0f.membersRequest\x1a\r.membersReply\"\x00\x62\x06proto3')



_MEMBERSREQUEST = DESCRIPTOR.message_types_by_name['membersRequest']
_MEMBERSREPLY = DESCRIPTOR.message_types_by_name['membersReply']
membersRequest = _reflection.GeneratedProtocolMessageType('membersRequest', (_message.Message,), {
  'DESCRIPTOR' : _MEMBERSREQUEST,
  '__module__' : 'groupservice_pb2'
  # @@protoc_insertion_point(class_scope:membersRequest)
  })
_sym_db.RegisterMessage(membersRequest)

membersReply = _reflection.GeneratedProtocolMessageType('membersReply', (_message.Message,), {
  'DESCRIPTOR' : _MEMBERSREPLY,
  '__module__' : 'groupservice_pb2'
  # @@protoc_insertion_point(class_scope:membersReply)
  })
_sym_db.RegisterMessage(membersReply)

_GROUPSERVICE = DESCRIPTOR.services_by_name['GroupService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MEMBERSREQUEST._serialized_start=22
  _MEMBERSREQUEST._serialized_end=56
  _MEMBERSREPLY._serialized_start=58
  _MEMBERSREPLY._serialized_end=89
  _GROUPSERVICE._serialized_start=91
  _GROUPSERVICE._serialized_end=153
# @@protoc_insertion_point(module_scope)