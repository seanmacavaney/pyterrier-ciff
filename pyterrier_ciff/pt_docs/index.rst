CIFF + PyTerrier
=====================================

   The Common Index File Format (CIFF) represents an attempt to build a binary data exchange format for
   open-source search engines to interoperate by sharing index structures.

   -- `CIFF Project <https://github.com/osirrc/ciff>`_

This PyTerrier extension provides access to `CIFF <https://github.com/osirrc/ciff>`_ files.
It provides the following core functionality:

- Build CIFF indexes from built indexes. `[example] <#building-from-an-index>`__
- Build CIFF indexes from learned sparse retrieval models. `[example] <#building-from-learned-sparse-models>`__
- Parse CIFF files to get the postings and document records. `[example] <#parsing-ciff-files>`__
- Share and load CIFF files to/from HuggingFace datasets. `[example] <#share-and-load-with-huggingface-datasets>`__

Quick Start
-------------------------------------

You can install ``pyterrier-ciff`` with pip:

.. code-block:: console
   :caption: Install ``pyterrier-ciff``

   $ pip install pyterrier-ciff

Building from an Index
-------------------------------------

Many indexes, such as those from Terrier and PISA, provide a ``get_corpus_iter()`` method that iterates
through the sparse representations. You can use use these methods with :func:`pyterrier_ciff.index`
to build construct a CIFF file:

.. tabs::

   .. tab:: Terrier

      .. code-block:: python
         :caption: Build a CIFF index from a Terrier index

         >>> import pyterrier as pt
         >>> import pyterrier_ciff
         >>> terrier_index = pt.IndexFactory.of('my_index.terrier')
         >>> pyterrier_ciff.index(terrier_index, 'my_index.ciff')
         CiffIndex('my_index.ciff')

   .. tab:: PISA

      .. code-block:: python
         :caption: Build a CIFF index from a PISA index

         >>> from pyterrier_pisa import PisaIndex
         >>> import pyterrier_ciff
         >>> pisa_index = PisaIndex('my_index.pisa')
         >>> pyterrier_ciff.index(pisa_index, 'my_index.ciff')
         CiffIndex('my_index.ciff')

.. note::

   :func:`pyterrier_ciff.index` uses reasonable default settings. You can customize more settings with
   :class:`~pyterrier_ciff.CiffIndexer` if you need more control over how the CIFF is constructed.

Building from Learned Sparse Models
-------------------------------------

Parsing CIFF Files
-------------------------------------

Share and Load with Huggingface Datasets
----------------------------------------

:class:`~pyterrier_ciff.CiffIndex` allows you to share your CIFF files on HuggingFace datasets using ``to_hf``:

.. code-block:: python
   :caption: Upload a CIFF index to HuggingFace

   >>> from pyterrier_ciff import CiffIndex
   >>> index = CiffIndex('my_index.ciff')
   >>> index.to_hf('username/my_index.ciff')

.. danger::

   Note that uploads to HuggingFace Datasets are public by default. Be sure not to upload an index that you
   are not allowed to share!


Similarly, you can download CIFF indexes that others have shared on HuggingFace using ``from_hf``:

.. code-block:: python
   :caption: Load a CIFF index from HuggingFace

   >>> from pyterrier_ciff import CiffIndex
   >>> index = CiffIndex.from_hf('username/my_index.ciff')

You can find `a list of available CIFF artifacts <https://huggingface.co/datasets?other=pyterrier-artifact.sparse_index.ciff>`__
on HuggingFace datasets.

.. note::

   ``to_hf`` and ``from_hf`` are provided by PyTerrier's :doc:`Artifact API </core/artifact>`. See that page for more details.

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
