# Derived from apify-client-python (docs/03_guides/code/01_input_async.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
import asyncio
from datetime import timedelta

from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    # Client initialization with the API token
    scrapely_client = ScrapelyClientAsync(token=TOKEN)

    # Get the Actor client
    actor_client = scrapely_client.actor('scrapely/instagram-hashtag-scraper')

    input_data = {'hashtags': ['rainbow'], 'resultsLimit': 20}

    # Run the Actor and wait up to 60 seconds for it to finish.
    # Input is not persisted for next runs.
    run_result = await actor_client.call(
        run_input=input_data, wait_duration=timedelta(seconds=60)
    )


if __name__ == '__main__':
    asyncio.run(main())
