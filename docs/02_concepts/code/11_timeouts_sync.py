# Derived from apify-client-python (docs/02_concepts/code/11_timeouts_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from datetime import timedelta

from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    # Configure default timeout tiers globally.
    scrapely_client = ScrapelyClient(
        token=TOKEN,
        timeout_short=timedelta(seconds=10),
        timeout_medium=timedelta(seconds=60),
        timeout_long=timedelta(seconds=600),
        timeout_max=timedelta(seconds=600),
    )

    dataset_client = scrapely_client.dataset('dataset-id')

    # Override the timeout for a single call using a timedelta.
    items = dataset_client.list_items(timeout=timedelta(seconds=120))

    # Or use a tier literal to select a predefined timeout.
    items = dataset_client.list_items(timeout='long')
