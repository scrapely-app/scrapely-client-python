# Derived from apify-client-python (docs/03_guides/code/04_pandas_async.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
import asyncio

import pandas as pd

from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    # Initialize the Scrapely client
    scrapely_client = ScrapelyClientAsync(token=TOKEN)
    actor_client = scrapely_client.actor('my-user/web-scraper')
    run_client = actor_client.last_run()
    dataset_client = run_client.dataset()

    # Load items from last dataset run
    dataset_data = await dataset_client.list_items()

    # Pass dataset items to Pandas DataFrame
    data_frame = pd.DataFrame(dataset_data.items)

    print(data_frame.info)


if __name__ == '__main__':
    asyncio.run(main())
