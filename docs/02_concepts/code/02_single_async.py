from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(TOKEN)

    # Resource clients accept an ID of the resource
    actor_client = scrapely_client.actor('username/actor-name')

    # Fetch the 'username/actor-name' object from the API
    my_actor = await actor_client.get()

    # Start the run of 'username/actor-name' and return the Run object
    my_actor_run = await actor_client.start()
