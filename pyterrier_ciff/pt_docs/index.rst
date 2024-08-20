CIFF + PyTerrier
=====================================

   The Common Index File Format (CIFF) represents an attempt to build a binary data exchange format for
   open-source search engines to interoperate by sharing index structures.

   -- `CIFF Project <https://github.com/osirrc/ciff>`_

This PyTerrier extension provides access to `CIFF <https://github.com/osirrc/ciff>`_ files.
It provides the following core functionality:

- Build CIFF indexes from built indexes. `[example] <#building-from-built-indexes>`__
- Build CIFF indexes from learned sparse retrieval models. `[example] <#building-from-learned-sparse-models>`__
- Parse CIFF files to get the postings and document records. `[example] <#parsing-ciff-files>`__
- Share and load CIFF files to/from HuggingFace datasets. `[example] <#share-and-load-with-huggingface-datasets>`__

Quick Start
-------------------------------------

You can install ``pyterrier-ciff`` with pip:

.. code-block:: console
   :caption: Install ``pyterrier-ciff``

   $ pip install pyterrier-ciff

Building from Built Indexes
-------------------------------------

Building from Learned Sparse Models
-------------------------------------

Parsing CIFF Files
-------------------------------------

Share and Load with Huggingface Datasets
----------------------------------------

Documentation
-------------------------------------

.. toctree::
   :maxdepth: 1

   API Documentation <api>
