# CIFF + PyTerrier

The Common Index File Format (CIFF) represents an attempt to build a binary data exchange format for open-source search engines to interoperate by sharing index structures.

-- [CIFF Project](https://github.com/osirrc/ciff)

[pyterrier-ciff](https://github.com/seanmacavaney/pyterrier-ciff) gives access to [CIFF](https://github.com/osirrc/ciff) files. It provides the following core functionality:

- Build CIFF indexes from built indexes. [example](https://pyterrier.readthedocs.io/en/latest/ext/pyterrier-ciff/index.html#building-from-an-index)
- Build CIFF indexes from learned sparse retrieval models.
- Parse CIFF files to get the postings and document records. [example](https://pyterrier.readthedocs.io/en/latest/ext/pyterrier-ciff/index.html#pyterrier_ciff.CiffIndex.records_iter)
- Share and load CIFF files to/from HuggingFace datasets. [example](https://pyterrier.readthedocs.io/en/latest/ext/pyterrier-ciff/index.html#building-from-an-index)
- Load files from the [CIFF Hub](https://github.com/pisa-engine/ciff-hub). [example](https://pyterrier.readthedocs.io/en/latest/ext/pyterrier-ciff/index.html#loading-ciff-from-the-ciff-hub)

## Quick Start

You can install `pyterrier-ciff` with pip:

```console
pip install pyterrier-ciff
```

## Documentation

Full documentation can be found in the [PyTerrier Docs](https://pyterrier.readthedocs.io/en/latest/ext/pyterrier-ciff/index.html).
