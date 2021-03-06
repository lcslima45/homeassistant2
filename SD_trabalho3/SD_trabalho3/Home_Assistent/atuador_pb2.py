# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: atuador.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='atuador.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\ratuador.proto\"\x17\n\x07\x63ommand\x12\x0c\n\x04info\x18\x01 \x01(\x05\"8\n\x06status\x12\x0e\n\x06\x63odigo\x18\x01 \x01(\x05\x12\x0c\n\x04nome\x18\x02 \x01(\t\x12\x10\n\x08mensagem\x18\x03 \x01(\t21\n\x0e\x61tuadorService\x12\x1f\n\x08sendInfo\x12\x08.command\x1a\x07.status\"\x00\x62\x06proto3'
)




_COMMAND = _descriptor.Descriptor(
  name='command',
  full_name='command',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='command.info', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=40,
)


_STATUS = _descriptor.Descriptor(
  name='status',
  full_name='status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='codigo', full_name='status.codigo', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nome', full_name='status.nome', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mensagem', full_name='status.mensagem', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=42,
  serialized_end=98,
)

DESCRIPTOR.message_types_by_name['command'] = _COMMAND
DESCRIPTOR.message_types_by_name['status'] = _STATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

command = _reflection.GeneratedProtocolMessageType('command', (_message.Message,), {
  'DESCRIPTOR' : _COMMAND,
  '__module__' : 'atuador_pb2'
  # @@protoc_insertion_point(class_scope:command)
  })
_sym_db.RegisterMessage(command)

status = _reflection.GeneratedProtocolMessageType('status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'atuador_pb2'
  # @@protoc_insertion_point(class_scope:status)
  })
_sym_db.RegisterMessage(status)



_ATUADORSERVICE = _descriptor.ServiceDescriptor(
  name='atuadorService',
  full_name='atuadorService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=100,
  serialized_end=149,
  methods=[
  _descriptor.MethodDescriptor(
    name='sendInfo',
    full_name='atuadorService.sendInfo',
    index=0,
    containing_service=None,
    input_type=_COMMAND,
    output_type=_STATUS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_ATUADORSERVICE)

DESCRIPTOR.services_by_name['atuadorService'] = _ATUADORSERVICE

# @@protoc_insertion_point(module_scope)
