from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)
    dataset_client = scrapely_client.dataset('dataset-id')

    # Lists items from the Actor's dataset.
    dataset_items = dataset_client.list_items().items
