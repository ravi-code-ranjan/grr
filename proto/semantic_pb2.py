# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grr/proto/semantic.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import google.protobuf.descriptor_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='grr/proto/semantic.proto',
  package='',
  serialized_pb='\n\x18grr/proto/semantic.proto\x1a google/protobuf/descriptor.proto\"\xb3\x01\n\x12SemanticDescriptor\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x14\n\x0c\x64ynamic_type\x18\x05 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12)\n\x05label\x18\x03 \x03(\x0e\x32\x1a.SemanticDescriptor.Labels\x12\x15\n\rfriendly_name\x18\x04 \x01(\t\"\"\n\x06Labels\x12\x0c\n\x08\x41\x44VANCED\x10\x01\x12\n\n\x06HIDDEN\x10\x02\"0\n\x19SemanticMessageDescriptor\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t:G\n\x08sem_type\x12\x1d.google.protobuf.FieldOptions\x18\xcc\xbf\xcc\x18 \x01(\x0b\x32\x13.SemanticDescriptor:P\n\x08semantic\x12\x1f.google.protobuf.MessageOptions\x18\xcb\xbf\xcc\x18 \x01(\x0b\x32\x1a.SemanticMessageDescriptor:9\n\x0b\x64\x65scription\x12!.google.protobuf.EnumValueOptions\x18\x9d\xb7\x99\x17 \x01(\t')


SEM_TYPE_FIELD_NUMBER = 51584972
sem_type = _descriptor.FieldDescriptor(
  name='sem_type', full_name='sem_type', index=0,
  number=51584972, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
SEMANTIC_FIELD_NUMBER = 51584971
semantic = _descriptor.FieldDescriptor(
  name='semantic', full_name='semantic', index=1,
  number=51584971, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
DESCRIPTION_FIELD_NUMBER = 48651165
description = _descriptor.FieldDescriptor(
  name='description', full_name='description', index=2,
  number=48651165, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=unicode("", "utf-8"),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)

_SEMANTICDESCRIPTOR_LABELS = _descriptor.EnumDescriptor(
  name='Labels',
  full_name='SemanticDescriptor.Labels',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ADVANCED', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HIDDEN', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=208,
  serialized_end=242,
)


_SEMANTICDESCRIPTOR = _descriptor.Descriptor(
  name='SemanticDescriptor',
  full_name='SemanticDescriptor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='SemanticDescriptor.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dynamic_type', full_name='SemanticDescriptor.dynamic_type', index=1,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='SemanticDescriptor.description', index=2,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='label', full_name='SemanticDescriptor.label', index=3,
      number=3, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='friendly_name', full_name='SemanticDescriptor.friendly_name', index=4,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SEMANTICDESCRIPTOR_LABELS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=63,
  serialized_end=242,
)


_SEMANTICMESSAGEDESCRIPTOR = _descriptor.Descriptor(
  name='SemanticMessageDescriptor',
  full_name='SemanticMessageDescriptor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='description', full_name='SemanticMessageDescriptor.description', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=244,
  serialized_end=292,
)

_SEMANTICDESCRIPTOR.fields_by_name['label'].enum_type = _SEMANTICDESCRIPTOR_LABELS
_SEMANTICDESCRIPTOR_LABELS.containing_type = _SEMANTICDESCRIPTOR;
DESCRIPTOR.message_types_by_name['SemanticDescriptor'] = _SEMANTICDESCRIPTOR
DESCRIPTOR.message_types_by_name['SemanticMessageDescriptor'] = _SEMANTICMESSAGEDESCRIPTOR

class SemanticDescriptor(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SEMANTICDESCRIPTOR

  # @@protoc_insertion_point(class_scope:SemanticDescriptor)

class SemanticMessageDescriptor(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SEMANTICMESSAGEDESCRIPTOR

  # @@protoc_insertion_point(class_scope:SemanticMessageDescriptor)

sem_type.message_type = _SEMANTICDESCRIPTOR
google.protobuf.descriptor_pb2.FieldOptions.RegisterExtension(sem_type)
semantic.message_type = _SEMANTICMESSAGEDESCRIPTOR
google.protobuf.descriptor_pb2.MessageOptions.RegisterExtension(semantic)
google.protobuf.descriptor_pb2.EnumValueOptions.RegisterExtension(description)

# @@protoc_insertion_point(module_scope)
