# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: takcontrol.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name='takcontrol.proto',
    package='',
    syntax='proto3',
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x10takcontrol.proto\">\n\nTakControl\x12\x17\n\x0fminProtoVersion\x18\x01 \x01(\r\x12\x17\n\x0fmaxProtoVersion\x18\x02 \x01(\rb\x06proto3'
)


_TAKCONTROL = _descriptor.Descriptor(
    name='TakControl',
    full_name='TakControl',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name='minProtoVersion', full_name='TakControl.minProtoVersion', index=0,
            number=1, type=13, cpp_type=3, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key),
        _descriptor.FieldDescriptor(
            name='maxProtoVersion', full_name='TakControl.maxProtoVersion', index=1,
            number=2, type=13, cpp_type=3, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key),
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
    serialized_start=20,
    serialized_end=82,
)

DESCRIPTOR.message_types_by_name['TakControl'] = _TAKCONTROL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TakControl = _reflection.GeneratedProtocolMessageType('TakControl', (_message.Message,), {
    'DESCRIPTOR': _TAKCONTROL,
    '__module__': 'takcontrol_pb2'
    # @@protoc_insertion_point(class_scope:TakControl)
})
_sym_db.RegisterMessage(TakControl)


# @@protoc_insertion_point(module_scope)
