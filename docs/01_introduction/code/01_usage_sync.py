# Derived from apify-client-python (docs/01_introduction/code/01_usage_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

# You can find your API token at https://api.scrape.ly
TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)

    # Start an Actor and wait for it to finish.
    actor_client = scrapely_client.actor('john-doe/my-cool-actor')
    call_result = actor_client.call()

    if call_result is None:
        print('Actor run failed.')
        return

    # Fetch results from the Actor run's default dataset.
    dataset_client = scrapely_client.dataset(call_result.default_dataset_id)
    list_items_result = dataset_client.list_items()
    print(f'Dataset: {list_items_result}')
