from typing import Any, BinaryIO, Dict, List, Optional

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


def _ciff_metadata_adapter(path: str, dir_listing: List[str]) -> Optional[Dict[str, Any]]:
    if len(dir_listing) == 1 and 'index.ciff' == dir_listing[0]:
        return {
            'type': 'sparse_index',
            'format': 'ciff',
            'package_hint': 'pyterrier-ciff',
        }
    if len(dir_listing) == 0 and path.endswith('.ciff'):
        return {
            'type': 'sparse_index',
            'format': 'ciff',
            'package_hint': 'pyterrier-ciff',
        }
