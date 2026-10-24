# Derived from apify-client-python (docs/01_introduction/code/03_input_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)
    actor_client = scrapely_client.actor('username/actor-name')

    # Define the input for the Actor.
    run_input = {
        'some': 'input',
    }

    # Start an Actor and wait for it to finish.
    call_result = actor_client.call(run_input=run_input)
