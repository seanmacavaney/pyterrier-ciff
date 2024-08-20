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

Many indexes, such as those from Terrier and PISA, provide a ``get_corpus_iter()`` method that iterates
through the sparse representations. You can use use these methods with :class:`~pyterrier_ciff.CiffIndexer`
to build construct a CIFF file:

.. code-block:: python
   :caption: Build a CIFF index from a Terrier index

   import pyterrier as pt
   import pyterrier_ciff
   terrier_index = pt.IndexFactory.of('my_index.terrier')
   pyterrier_ciff.index(terrier_index, 'my_index.ciff')

.. code-block:: python
   :caption: Build a CIFF index from a PISA index

   from pyterrier_pisa import PisaIndex
   import pyterrier_ciff
   pisa_index = PisaIndex('my_index.pisa')
   pyterrier_ciff.index(pisa_index, 'my_index.ciff')

Building from Learned Sparse Models
-------------------------------------

Parsing CIFF Files
-------------------------------------

Share and Load with Huggingface Datasets
----------------------------------------

Documentation
-------------------------------------

The complete API documentation can be found here:

.. toctree::
   :maxdepth: 1

   API Documentation <api>

Citation
-------------------------------------

.. code-block:: bibtex
   :caption: CIFF Citation

   @inproceedings{DBLP:conf/sigir/LinMKMMSTV20,
     author       = {Jimmy Lin and
                     Joel M. Mackenzie and
                     Chris Kamphuis and
                     Craig Macdonald and
                     Antonio Mallia and
                     Michal Siedlaczek and
                     Andrew Trotman and
                     Arjen P. de Vries},
     title        = {Supporting Interoperability Between Open-Source Search Engines with
                     the Common Index File Format},
     booktitle    = {Proceedings of the 43rd International {ACM} {SIGIR} conference on
                     research and development in Information Retrieval, {SIGIR} 2020, Virtual
                     Event, China, July 25-30, 2020},
     pages        = {2149--2152},
     publisher    = {{ACM}},
     year         = {2020},
     url          = {https://doi.org/10.1145/3397271.3401404},
     doi          = {10.1145/3397271.3401404}
   }
