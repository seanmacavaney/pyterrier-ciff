# flake8: noqa
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: ciff.proto
# Protobuf Python Version: 5.27.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    3,
    '',
    'ciff.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nciff.proto\x12\x0eio.osirrc.ciff\"\xcc\x01\n\x06Header\x12\x0f\n\x07version\x18\x01 \x01(\x05\x12\x1a\n\x12num_postings_lists\x18\x02 \x01(\x05\x12\x10\n\x08num_docs\x18\x03 \x01(\x05\x12\x1c\n\x14total_postings_lists\x18\x04 \x01(\x05\x12\x12\n\ntotal_docs\x18\x05 \x01(\x05\x12!\n\x19total_terms_in_collection\x18\x06 \x01(\x03\x12\x19\n\x11\x61verage_doclength\x18\x07 \x01(\x01\x12\x13\n\x0b\x64\x65scription\x18\x08 \x01(\t\"$\n\x07Posting\x12\r\n\x05\x64ocid\x18\x01 \x01(\x05\x12\n\n\x02tf\x18\x02 \x01(\x05\"_\n\x0cPostingsList\x12\x0c\n\x04term\x18\x01 \x01(\t\x12\n\n\x02\x64\x66\x18\x02 \x01(\x03\x12\n\n\x02\x63\x66\x18\x03 \x01(\x03\x12)\n\x08postings\x18\x04 \x03(\x0b\x32\x17.io.osirrc.ciff.Posting\"G\n\tDocRecord\x12\r\n\x05\x64ocid\x18\x01 \x01(\x05\x12\x18\n\x10\x63ollection_docid\x18\x02 \x01(\t\x12\x11\n\tdoclength\x18\x03 \x01(\x05\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ciff_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_HEADER']._serialized_start=31
  _globals['_HEADER']._serialized_end=235
  _globals['_POSTING']._serialized_start=237
  _globals['_POSTING']._serialized_end=273
  _globals['_POSTINGSLIST']._serialized_start=275
  _globals['_POSTINGSLIST']._serialized_end=370
  _globals['_DOCRECORD']._serialized_start=372
  _globals['_DOCRECORD']._serialized_end=443
# @@protoc_insertion_point(module_scope)
