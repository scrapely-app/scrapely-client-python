# Derived from apify-client-python (docs/02_concepts/code/10_default_http_client_async.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from datetime import timedelta

from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    client = ScrapelyClientAsync(
        token=TOKEN,
        max_retries=4,
        min_delay_between_retries=timedelta(milliseconds=500),
        timeout_medium=timedelta(seconds=360),
    )
