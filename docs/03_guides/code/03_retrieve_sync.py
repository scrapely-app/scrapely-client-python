# Derived from apify-client-python (docs/03_guides/code/03_retrieve_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    # Client initialization with the API token
    scrapely_client = ScrapelyClient(token=TOKEN)
    actor_client = scrapely_client.actor('echofield/instagram-hashtag-scraper')
    runs_client = actor_client.runs()

    # See pagination to understand how to get more runs
    actor_runs = runs_client.list(limit=20)

    datasets_client = scrapely_client.datasets()
    merging_dataset = datasets_client.get_or_create(name='merge-dataset')

    for run in actor_runs.items:
        # Each run saves its results to its default dataset (items can be paginated)
        dataset_client = scrapely_client.dataset(run.default_dataset_id)
        dataset_items = dataset_client.list_items(limit=1000)

        # Items can be pushed to single dataset
        merging_dataset_client = scrapely_client.dataset(merging_dataset.id)
        merging_dataset_client.push_items(dataset_items.items)

        # ...


if __name__ == '__main__':
    main()
