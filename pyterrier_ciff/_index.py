import io
import json
from pathlib import Path
from typing import Iterator, Tuple, Union

import pyterrier as pt
import pyterrier_alpha as pta

import pyterrier_ciff
from pyterrier_ciff import DocRecord, Header, PostingsList
from pyterrier_ciff._utils import protobuf_read_delimited_into


class CiffIndex(pta.Artifact):
    ARTIFACT_TYPE = 'sparse_index'
    ARTIFACT_FORMAT = 'ciff'

    """Represents a."""
    def indexer(self,
        *,
        scale: float = 100.,
        description: str = 'pyterrier-ciff',
        verbose: bool = True
    ) -> pt.Indexer:
        return pyterrier_ciff.CiffIndexer(self, scale=scale, description=description, verbose=verbose)

    def built(self) -> bool:
        return self.ciff_file_path().exists()

    def ciff_file_path(self) -> Path:
        if self.path.is_dir():
            return self.path/'index.ciff'
        if str(self.path).endswith('.ciff'):
            return self.path
        if not self.path.exists():
            self.path.mkdir(parents=True, exist_ok=True)
        return self.path/'index.ciff'

    def header(self) -> Header:
        assert self.built()
        with self.ciff_file_path().open('rb') as ciff_in:
            header = pyterrier_ciff.Header()
            protobuf_read_delimited_into(ciff_in, header)
        return header

    def records_iter(self) -> Iterator[Union[PostingsList, DocRecord]]:
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
