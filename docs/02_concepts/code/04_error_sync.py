from scrapely_client import ScrapelyClient
from scrapely_client.errors import ScrapelyApiError, NotFoundError

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)

    try:
        # Try to list items from a non-existing dataset.
        dataset_client = scrapely_client.dataset('non-existing-dataset-id')
        dataset_items = dataset_client.list_items().items
    except NotFoundError:
        # 404 — branch on a specific subclass when you want to react to it.
        dataset_items = []
    except ScrapelyApiError as err:
        # Catch-all for every other API error.
        print(f'API error: {err}')
        dataset_items = []

    print(f'Fetched {len(dataset_items)} items.')


if __name__ == '__main__':
    main()
