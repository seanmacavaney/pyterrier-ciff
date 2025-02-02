import os
from pathlib import Path
from urllib.parse import ParseResult

import pyterrier_alpha as pta


def _ciff_hub_url_resolver(parsed_url: ParseResult) -> str:
    """Resolve URLs from the CIFF hub.

    For instance: ``Artifact.from_url("ciff-hub:esplade/bp-msmarco-passage-esplade-quantized")``
    or ``CiffIndex.from_ciff_hub("esplade/bp-msmarco-passage-esplade-quantized")``
    """
    if parsed_url.path.count('/') != 1:
        return None # invalid
    parent_id, ciff_id = parsed_url.path.split('/')
    url = f'https://storage.googleapis.com/ciff-hub/{parent_id}/ciff/{ciff_id}.ciff'
    cache = Path(os.environ.get('CIFF_HUB_CACHE', os.path.expanduser('~/.cache/ciff-hub/')))
    target_path = cache / parent_id / (ciff_id + '.ciff')
    if not target_path.parent.exists():
        target_path.parent.mkdir(parents=True)
        pta.io.download(url, target_path)
    return str(target_path)
