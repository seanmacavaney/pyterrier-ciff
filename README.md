# CIFF + PyTerrier

The Common Index File Format (CIFF) represents an attempt to build a binary data exchange format for open-source search engines to interoperate by sharing index structures.

-- [CIFF Project](https://github.com/osirrc/ciff)

[pyterrier-ciff](https://github.com/seanmacavaney/pyterrier-ciff) gives access to [CIFF](https://github.com/osirrc/ciff) files. It provides the following core functionality:

- Build CIFF indexes from built indexes. [example](#building-from-an-index)
- Build CIFF indexes from learned sparse retrieval models. [example](#building-from-learned-sparse-models)
- Parse CIFF files to get the postings and document records. [example](#parsing-ciff-files)
- Share and load CIFF files to/from HuggingFace datasets. [example](#share-and-load-with-huggingface-datasets)

## Quick Start

You can install `pyterrier-ciff` with pip:

```console
pip install pyterrier-ciff
```

## Documentation

Full documentation can be found in the [PyTerrier Docs](https://pyterrier.readthedocs.io/en/latest/ext/pyterrier-ciff/index.html).
