# Derived from apify-client-python (docs/02_concepts/code/07_call_async.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(TOKEN)
    actor_client = scrapely_client.actor('username/actor-name')

    # Start an Actor and wait for it to finish.
    finished_actor_run = await actor_client.call()

    # Start an Actor and wait up to 60 seconds for it to finish.
    actor_run = await actor_client.start(wait_for_finish=60)
