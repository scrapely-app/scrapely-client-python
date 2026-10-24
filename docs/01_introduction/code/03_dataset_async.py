# Derived from apify-client-python (docs/01_introduction/code/03_dataset_async.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(TOKEN)
    dataset_client = scrapely_client.dataset('dataset-id')

    # Lists items from the Actor's dataset.
    dataset_items = (await dataset_client.list_items()).items
