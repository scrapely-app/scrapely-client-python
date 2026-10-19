# Derived from apify-client-python (Copyright Apify Technologies s.r.o., Apache-2.0).
# Modified by TeraShift GmbH. See the LICENSE and NOTICE files.
from scrapely_client._utils.try_import import install_import_hook as _install_import_hook
from scrapely_client._utils.try_import import try_import as _try_import

# These imports have only mandatory dependencies, so they are imported directly.
from scrapely_client.http_compressors._base import HttpCompressor
from scrapely_client.http_compressors._gzip import GzipHttpCompressor

_install_import_hook(__name__)

# `brotli` is an optional extra, so it's wrapped in try_import. Accessing `BrotliHttpCompressor`
# without the extra installed raises a clear ImportError instead of failing at package import time.
with _try_import(__name__, 'BrotliHttpCompressor', dependency_name='brotli') as _brotli_import:
    from scrapely_client.http_compressors._brotli import BrotliHttpCompressor

if _brotli_import.available:
    __all__ = ['BrotliHttpCompressor', 'GzipHttpCompressor', 'HttpCompressor']
else:
    __all__ = ['GzipHttpCompressor', 'HttpCompressor']
