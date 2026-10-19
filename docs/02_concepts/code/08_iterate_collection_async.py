from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(TOKEN)

    # Iterate over all Actors owned by the current user, lazily fetching
    # as many pages as needed under the hood.
    async for actor in scrapely_client.actors().iterate(my=True):
        print(actor.id)
