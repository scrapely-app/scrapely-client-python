# Derived from apify-client-python (docs/02_concepts/code/02_collection_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)

    # Collection clients do not require a parameter
    actor_collection_client = scrapely_client.actors()

    # Create an Actor with the name: my-actor
    my_actor = actor_collection_client.create(name='my-actor')

    # List all of your Actors
    actor_list = actor_collection_client.list().items
