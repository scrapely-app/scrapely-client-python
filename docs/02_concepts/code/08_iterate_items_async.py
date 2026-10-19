from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(TOKEN)
    dataset_client = scrapely_client.dataset('dataset-id')

    # Define the pagination parameters
    limit = 1500  # Number of items in total
    offset = 100  # Starting offset

    # Iterate through items automatically, lazily sending as many API calls
    # as needed and receiving items in chunks.
    async for item in dataset_client.iterate_items(limit=limit, offset=offset):
        print(item)  # Process the item as needed
