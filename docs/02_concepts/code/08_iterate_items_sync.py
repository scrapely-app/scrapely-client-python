# Derived from apify-client-python (docs/02_concepts/code/08_iterate_items_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)
    dataset_client = scrapely_client.dataset('dataset-id')

    # Define the pagination parameters
    limit = 1500  # Number of items in total
    offset = 100  # Starting offset

    # Iterate through items automatically, lazily sending as many API calls
    # as needed and receiving items in chunks.
    for item in dataset_client.iterate_items(limit=limit, offset=offset):
        print(item)  # Process the item as needed


if __name__ == '__main__':
    main()
