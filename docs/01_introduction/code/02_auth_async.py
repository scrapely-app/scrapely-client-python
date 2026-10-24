# Derived from apify-client-python (docs/01_introduction/code/02_auth_async.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    # Client initialization with the API token.
    scrapely_client = ScrapelyClientAsync(TOKEN)
