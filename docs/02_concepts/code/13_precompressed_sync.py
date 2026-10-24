# Derived from apify-client-python (docs/02_concepts/code/13_precompressed_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
import gzip
from pathlib import Path

from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)
    kvs_client = scrapely_client.key_value_store('MY-KVS-ID')

    report = Path('report.csv').read_bytes()
    compressed_report = gzip.compress(report)

    # The explicit content encoding stops the client from compressing the bytes again.
    kvs_client.set_record(
        'report',
        compressed_report,
        content_type='text/csv',
        content_encoding='gzip',
    )
