# Derived from apify-client-python (docs/02_concepts/code/13_skip_compression_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from pathlib import Path

from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)
    kvs_client = scrapely_client.key_value_store('MY-KVS-ID')

    screenshot = Path('screenshot.png').read_bytes()

    # The explicit content type lets the client skip compressing the PNG.
    kvs_client.set_record('screenshot', screenshot, content_type='image/png')
