import io
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, Protocol, Union, runtime_checkable

import pyterrier as pt
import pyterrier_alpha as pta

from pyterrier_ciff import CiffIndex, DocRecord, Header, PostingsList, invert
from pyterrier_ciff._utils import protobuf_write_delimited_to


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
            total_terms_in_collection = 0
            total_postings_lists = 0
            total_docs = 0
            with (tmp/'postings').open('w+b') as out_postings, \
                 (tmp/'docno').open('w+b') as out_docs:
                for rtype, record in invert(inp, scale=self.scale, verbose=self.verbose):
                    if rtype == 'doc':
                        total_docs += 1
                        doc_length = int(record.tfs.sum())
                        total_terms_in_collection += doc_length
                        doc = DocRecord()
                        doc.docid = record.did
                        doc.collection_docid = record.docno
                        doc.doclength = doc_length
                        protobuf_write_delimited_to(doc, out_docs)
                    elif rtype == 'term':
                        total_postings_lists += 1
                        posting_list = PostingsList()
                        posting_list.term = record.term
                        record.dids[1:] = record.dids[1:] - record.dids[:-1] # gap encoding
                        for i in range(record.dids.shape[0]):
                            posting = posting_list.postings.add()
                            posting.docid = record.dids[i]
                            posting.tf = record.tfs[i]
                        posting_list.df = int(record.tfs.shape[0])
                        posting_list.cf = int(record.tfs.sum())
                        protobuf_write_delimited_to(posting_list, out_postings)
                with pta.io.finalized_open(self._index.ciff_file_path(), 'b') as out_ciff:
                    header = Header()
                    header.version = 1
                    header.num_postings_lists = total_postings_lists
                    header.num_docs = total_docs
                    header.total_postings_lists = total_postings_lists
                    header.total_docs = total_docs
                    header.total_terms_in_collection = total_terms_in_collection
                    header.average_doclength = total_terms_in_collection / total_docs
                    header.description = self.description
                    protobuf_write_delimited_to(header, out_ciff)
                    out_postings.seek(0)
                    while out_postings.peek():
                        out_ciff.write(out_postings.read(io.DEFAULT_BUFFER_SIZE)) # copy over in chunks
                    out_docs.seek(0)
                    while out_docs.peek():
                        out_ciff.write(out_docs.read(io.DEFAULT_BUFFER_SIZE)) # copy over in chunks
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
    return CiffIndexer(ciff_path, scale=1.).index(inp)
