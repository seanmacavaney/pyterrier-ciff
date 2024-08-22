import tempfile
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Any, BinaryIO, Dict, Iterable, List, Tuple

import numpy as np
import pyterrier as pt

_BUFFER_SIZE = 4096
_BUFFER_READ_SIZE = _BUFFER_SIZE * 4 # 4 bytes in uint32


@dataclass
class _PostingBuffer:
    term_id: int
    buffer_idx: int = 0
    buffer_did: np.ndarray = field(default_factory=list)
    buffer_tf: np.ndarray = field(default_factory=list)
    file_chunk_offsets: List[int] = field(default_factory=list)

    def add(self, did: int, tf: int, scratch: BinaryIO):
        self.buffer_did.append(did)
        self.buffer_tf.append(tf)
        self.buffer_idx += 1

        # Flush to disk if needed
        if self.buffer_idx == _BUFFER_SIZE:
            self.file_chunk_offsets.append(scratch.tell())
            scratch.write(np.array(self.buffer_did, dtype=np.uint32).tobytes())
            scratch.write(np.array(self.buffer_tf, dtype=np.uint32).tobytes())
            self.buffer_did.clear()
            self.buffer_tf.clear()
            self.buffer_idx = 0

    def load(self, scratch: BinaryIO) -> Tuple[np.array, np.array]:
        dids = []
        tfs = []
        for offset in self.file_chunk_offsets:
            scratch.seek(offset)
            dids.append(np.frombuffer(scratch.read(_BUFFER_READ_SIZE), dtype=np.uint32))
            tfs.append(np.frombuffer(scratch.read(_BUFFER_READ_SIZE), dtype=np.uint32))
        if self.buffer_idx > 0:
            dids.append(np.array(self.buffer_did[:self.buffer_idx], dtype=np.uint32))
            tfs.append(np.array(self.buffer_tf[:self.buffer_idx], dtype=np.uint32))
        if len(dids) > 0:
            dids = np.concatenate(dids)
            tfs = np.concatenate(tfs)
        else:
            dids = dids[0]
            tfs = tfs[0]
        return dids, tfs


def invert(inp: Iterable[Dict[str, Any]], *, scale: float = 100., verbose: bool = False):
    """Inverts the provided stream of documents, calling ``on_doc`` and ``on_term`` along the way.

    Args:
        inp: An iterable with ``docno`` and ``toks`` fields.
        scale: The scaling factor for term frequencies. Defaults to 100.
        verbose: Whether to show a progress bar. Defaults to False.
    """
    with tempfile.TemporaryFile() as scratch:
        buffer = {}
        if verbose:
            inp = pt.tqdm(inp, unit='doc', desc='inverting')
        for did, doc in enumerate(inp):
            tids = []
            tfs = []
            for term, weight in doc['toks'].items():
                tf = int(weight * scale)
                if tf <= 0:
                    # Not indexed
                    continue
                if term not in buffer:
                    buffer[term] = _PostingBuffer(term_id=len(buffer))
                b = buffer[term]
                tids.append(b.term_id)
                tfs.append(tf)
                # Update the buffer entry and flush (if needed)
                b.add(did, tf, scratch)
            yield {
                'type': 'doc',
                'did': did,
                'docno': doc['docno'],
                'tids': np.array(tids, dtype=np.uint32),
                'tfs': np.array(tfs, dtype=np.uint32),
            }

        it = buffer.items()
        if verbose:
            it = pt.tqdm(it, unit='term', desc='posting')
        for term, buf in it:
            dids, tfs = buf.load(scratch)
            yield {
                'type': 'term',
                'tid': buf.term_id,
                'term': term,
                'dids': dids,
                'tfs': tfs,
            }
