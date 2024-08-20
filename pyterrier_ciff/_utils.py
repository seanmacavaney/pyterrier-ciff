from typing import Any, BinaryIO

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes


def protobuf_read_delimited_into(file: BinaryIO, obj: Any):
    read_size, advance = _DecodeVarint32(file.peek(), 0)
    file.read(advance)
    obj.ParseFromString(file.read(read_size))


def protobuf_write_delimited_to(obj: Any, file: BinaryIO):
    enc = obj.SerializeToString()
    file.write(_VarintBytes(len(enc)))
    file.write(enc)
