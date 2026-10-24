# Derived from apify-client-python (docs/02_concepts/code/08_iterate_collection_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)

    # Iterate over all Actors owned by the current user, lazily fetching
    # as many pages as needed under the hood.
    for actor in scrapely_client.actors().iterate(my=True):
        print(actor.id)


if __name__ == '__main__':
    main()
