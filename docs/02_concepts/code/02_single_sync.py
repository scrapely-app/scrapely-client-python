# Derived from apify-client-python (docs/02_concepts/code/02_single_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)

    # Resource clients accept an ID of the resource
    actor_client = scrapely_client.actor('username/actor-name')

    # Fetch the 'username/actor-name' object from the API
    my_actor = actor_client.get()

    # Start the run of 'username/actor-name' and return the Run object
    my_actor_run = actor_client.start()
