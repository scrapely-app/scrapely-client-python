from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)
    actor_client = scrapely_client.actor('username/actor-name')

    # Start an Actor and wait for it to finish.
    finished_actor_run = actor_client.call()

    # Start an Actor and wait up to 60 seconds for it to finish.
    actor_run = actor_client.start(wait_for_finish=60)
