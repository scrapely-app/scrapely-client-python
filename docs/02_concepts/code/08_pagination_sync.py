from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)

    # Initialize the dataset client
    dataset_client = scrapely_client.dataset('dataset-id')

    # Define the pagination parameters
    limit = 1000  # Number items to request from API
    offset = 0  # Starting offset

    # Send single API call to fetch paginated items.
    # (number of items per single call can be limited by API)
    paginated_items = dataset_client.list_items(limit=limit, offset=offset)

    # Inspect pagination metadata returned by API
    print(paginated_items.total)

    for item in paginated_items.items:
        print(item)  # Process the item as needed
