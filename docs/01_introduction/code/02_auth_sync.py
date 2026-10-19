from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    # Client initialization with the API token.
    scrapely_client = ScrapelyClient(TOKEN)
