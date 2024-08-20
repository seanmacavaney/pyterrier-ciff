"""Top-level package for PyTerrier CIFF."""

__version__ = '0.1.0'

from pyterrier_ciff._ciff_pb2 import DocRecord, Header, Posting, PostingsList
from pyterrier_ciff._index import CiffIndex
from pyterrier_ciff._indexer import CiffIndexer, index

__all__ = [
    'CiffIndex', 'CiffIndexer', 'index',

    # protobuf
    'DocRecord', 'Header', 'Posting', 'PostingsList',
]
