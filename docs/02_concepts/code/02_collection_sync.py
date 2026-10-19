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
