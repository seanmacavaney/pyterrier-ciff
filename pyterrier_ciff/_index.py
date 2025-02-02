import io
import json
from pathlib import Path
from typing import Iterator, Tuple, Union

import pyterrier as pt
import pyterrier_alpha as pta

import pyterrier_ciff
from pyterrier_ciff import DocRecord, Header, PostingsList
from pyterrier_ciff._utils import protobuf_read_delimited_into


class CiffIndex(pt.Artifact):
    """Represents a CIFF "index" file.

    CIFF files are a compact binary format for storing and sharing inverted indexes using `Protocol Buffers
    <https://protobuf.dev/>`_.
    """

    ARTIFACT_TYPE = 'sparse_index'
    ARTIFACT_FORMAT = 'ciff'

    def __init__(self, path: Union[str, Path]):
        """Create a reference to CIFF index.

        Args:
            path: The path to the CIFF file or directory containing the CIFF file. If the path does not exit, it must
                be built using ``indexer()`` before it can be used.
        """
        super().__init__(path)

    def indexer(self,
        *,
        scale: float = 100.,
        description: str = 'pyterrier-ciff',
        verbose: bool = True
    ) -> pt.Indexer:
        """Create a CIFF indexer.

        The indexer accepts an iterable with a docno and toks fields.

        Args:
            scale: The scaling factor for term frequencies. Defaults to 100.
            description: The description of the index. Defaults to 'pyterrier-ciff'.
            verbose: Whether to show a progress bar. Defaults to True.
        """
        return pyterrier_ciff.CiffIndexer(self, scale=scale, description=description, verbose=verbose)

    def built(self) -> bool:
        """Check if the index has been built."""
        return self.ciff_file_path().exists()

    def ciff_file_path(self) -> Path:
        """Get the path to the CIFF file."""
        if self.path.is_dir():
            return self.path/'index.ciff'
        if str(self.path).endswith('.ciff'):
            return self.path
        if not self.path.exists():
            self.path.mkdir(parents=True, exist_ok=True)
        return self.path/'index.ciff'

    def header(self) -> Header:
        """Get the header of the CIFF file (if it has been built)."""
        assert self.built()
        with self.ciff_file_path().open('rb') as ciff_in:
            header = pyterrier_ciff.Header()
            protobuf_read_delimited_into(ciff_in, header)
        return header

    def records_iter(self) -> Iterator[Union[PostingsList, DocRecord]]:
        """Iterate over the PostingsList and DocRecord records in the CIFF file (if it has been built)."""
        assert self.built()
        with self.ciff_file_path().open('rb') as ciff_in:
            header = pyterrier_ciff.Header()
            protobuf_read_delimited_into(ciff_in, header)
            postings_list = pyterrier_ciff.PostingsList()
            doc_record = pyterrier_ciff.DocRecord()
            for _ in range(header.num_postings_lists):
                protobuf_read_delimited_into(ciff_in, postings_list)
                yield postings_list
            for _ in range(header.num_docs):
                protobuf_read_delimited_into(ciff_in, doc_record)
                yield doc_record

    def __iter__(self) -> Iterator[Union[PostingsList, DocRecord]]:
        return self.records_iter()

    def _package_files(self) -> Iterator[Tuple[str, Union[str, io.BytesIO]]]:
        if not self.path.is_dir() and str(self.path).endswith('.ciff'):
            yield 'index.ciff', self.path
            yield 'pt_meta.json', io.BytesIO(json.dumps(self._build_metadata()).encode())
        else:
            yield from super()._package_files()

    def __repr__(self):
        return f'CiffIndex({str(self.path)!r})'

    @staticmethod
    def from_ciff_hub(name: str) -> 'CiffIndex':
        """Loads a CIFF index from the `CIFF Hub <https://github.com/pisa-engine/ciff-hub>`__.

        Args:
            name: The name of the CIFF file in CIFF Hub, e.g., ``esplade/bp-msmarco-passage-esplade-quantized``

        Returns:
            :class:`~pyterrier_ciff.CiffIndex`: The CIFF index downloaded from the hub.
        """
        return CiffIndex.from_url(f'ciff-hub:{name}')
