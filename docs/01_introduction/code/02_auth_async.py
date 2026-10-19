from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    # Client initialization with the API token.
    scrapely_client = ScrapelyClientAsync(TOKEN)
