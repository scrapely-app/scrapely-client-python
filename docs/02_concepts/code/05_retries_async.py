# Derived from apify-client-python (docs/02_concepts/code/05_retries_async.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from datetime import timedelta

from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(
        token=TOKEN,
        max_retries=4,
        min_delay_between_retries=timedelta(milliseconds=500),
        timeout_short=timedelta(seconds=5),
        timeout_medium=timedelta(seconds=30),
        timeout_long=timedelta(seconds=360),
        timeout_max=timedelta(seconds=360),
    )
