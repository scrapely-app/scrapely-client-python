# Derived from apify-client-python (docs/01_introduction/code/02_auth_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    # Client initialization with the API token.
    scrapely_client = ScrapelyClient(TOKEN)
