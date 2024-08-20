import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, BinaryIO, Dict, Iterable, List, Protocol, Union, runtime_checkable

import numpy as np
import pyterrier as pt
import pyterrier_alpha as pta

from pyterrier_ciff import CiffIndex, DocRecord, Header, PostingsList
from pyterrier_ciff._utils import protobuf_write_delimited_to

_BUFFER_SIZE = 4096
_BUFFER_READ_SIZE = _BUFFER_SIZE * 4 # 4 bytes in uint32


@dataclass
class _PostingBuffer:
    prev_did: int = 0
    buffer_idx: int = 0
    buffer_did: np.ndarray = field(default_factory=list)
    buffer_tf: np.ndarray = field(default_factory=list)
    file_chunk_offsets: List[int] = field(default_factory=list)

    def add(self, did: int, tf: int, out_did: BinaryIO, out_tf: BinaryIO):
        did_gap = did - self.prev_did
        self.prev_did = did
        self.buffer_did.append(did_gap)
        self.buffer_tf.append(tf)
        self.buffer_idx += 1

        # Flush to disk if needed
        if self.buffer_idx == _BUFFER_SIZE:
            self.file_chunk_offsets.append(out_did.tell())
            out_did.write(np.array(self.buffer_did, dtype=np.uint32).tobytes())
            out_tf.write(np.array(self.buffer_tf, dtype=np.uint32).tobytes())
            self.buffer_did.clear()
            self.buffer_tf.clear()
            self.buffer_idx = 0

    def to_protobuf_posting_list(self, term: str, out_did: BinaryIO, out_tf: BinaryIO) -> PostingsList:
        pl = PostingsList()
        pl.term = term
        total = 0
        for offset in self.file_chunk_offsets:
            out_did.seek(offset)
            out_tf.seek(offset)
            dids = np.frombuffer(out_did.read(_BUFFER_READ_SIZE), dtype=np.uint32)
            tfs = np.frombuffer(out_tf.read(_BUFFER_READ_SIZE), dtype=np.uint32)
            total += tfs.sum()
            for i in range(_BUFFER_SIZE):
                posting = pl.postings.add()
                posting.docid = dids[i]
                posting.tf = tfs[i]
        total += sum(self.buffer_tf)
        for i in range(self.buffer_idx):
            posting = pl.postings.add()
            posting.docid = self.buffer_did[i]
            posting.tf = self.buffer_tf[i]
        pl.df = len(self.file_chunk_offsets) * _BUFFER_SIZE + self.buffer_idx
        pl.cf = int(total)
        return pl


class CiffIndexer(pt.Indexer):
    """An indexer that produces a :class:`~pyterrier_ciff.CiffIndex`."""
    def __init__(self,
        index: Union[CiffIndex, str],
        *,
        scale: float = 100.,
        description: str = 'pyterrier-ciff',
        verbose: bool = True
    ):
        """Create a CIFF indexer.

        Args:
            index: A CIFF index object or the path to the CIFF file to create.
            scale: The scaling factor for term frequencies. Defaults to 100.
            description: The description of the index. Defaults to 'pyterrier-ciff'.
            verbose: Whether to show a progress bar. Defaults to True.
        """
        self._index = index if isinstance(index, CiffIndex) else CiffIndex(index)
        self.scale = scale
        self.description = description
        self.verbose = verbose

    def index(self, inp: Iterable[Dict[str, Any]]) -> CiffIndex:
        """Index the input documents.

        Args:
            inp: An iterable with ``docno`` and ``toks`` fields.

        Returns:
            The built CIFF index.
        """
        assert not self._index.built()

        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            buffer = {}
            doc_rec = DocRecord()
            doc_count = 0
            term_count = 0
            with (tmp/'did.u4').open('w+b') as out_did, \
                 (tmp/'tf.u4').open('w+b') as out_tf, \
                 (tmp/'docno').open('w+b') as out_docs:
                if self.verbose:
                    inp = pt.tqdm(inp, unit='d', desc='ciff-invert')
                for did, doc in enumerate(inp):
                    doc_length = 0
                    for tok, weight in doc['toks'].items():
                        tf = int(weight * self.scale)
                        if tf <= 0:
                            # Not indexed
                            continue
                        doc_length += tf
                        if tok not in buffer:
                            buffer[tok] = _PostingBuffer()
                        # Update the buffer entry and flush (if needed)
                        buffer[tok].add(did, tf, out_did, out_tf)

                    doc_count += 1
                    term_count += doc_length
                    doc_rec.docid = did
                    doc_rec.collection_docid = doc['docno']
                    doc_rec.doclength = doc_length
                    protobuf_write_delimited_to(doc_rec, out_docs)

                with pta.io.finalized_open(self._index.ciff_file_path(), 'b') as out_ciff:
                    header = Header()
                    header.version = 1
                    header.num_postings_lists = len(buffer)
                    header.num_docs = doc_count
                    header.total_postings_lists = len(buffer)
                    header.total_docs = doc_count
                    header.total_terms_in_collection = term_count
                    header.average_doclength = term_count / doc_count
                    header.description = self.description
                    protobuf_write_delimited_to(header, out_ciff)

                    it = sorted(buffer.items())
                    if self.verbose:
                        it = pt.tqdm(it, unit='term', desc='ciff-postings')
                    for tok, buf in it:
                        posting_list = buf.to_protobuf_posting_list(tok, out_did, out_tf)
                        protobuf_write_delimited_to(posting_list, out_ciff)

                    out_docs.seek(0)
                    while out_docs.peek():
                        out_ciff.write(out_docs.read(16384)) # copy over in 16kb chunks
        return self._index

@runtime_checkable
class HasGetCorpusIter(Protocol):
    def get_corpus_iter(self) -> Iterable[Dict[str, Any]]: ...


def index(inp: Union[HasGetCorpusIter, Iterable[Dict[str, Any]]], ciff_path: str) -> CiffIndex:
    """Index the input to the provided path.

    Args:
        inp: An iterable of documents to index to CIFF, or an object that exposes a ``get_corpus_iter`` method.
        ciff_path: The path to write the CIFF index.

    Returns:
        The built CIFF index.
    """
    if isinstance(inp, HasGetCorpusIter):
        inp = inp.get_corpus_iter()
    return CiffIndexer(ciff_path).index(inp)
