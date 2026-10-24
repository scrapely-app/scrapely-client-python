# Derived from apify-client-python (docs/02_concepts/code/03_nested_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)

    actor_client = scrapely_client.actor('username/actor-name')
    runs_client = actor_client.runs()

    # List the last 10 runs of the Actor.
    actor_runs = runs_client.list(limit=10, desc=True).items

    # Select the last run of the Actor that finished with a SUCCEEDED status.
    last_succeeded_run_client = actor_client.last_run(status='SUCCEEDED')

    # Get dataset
    actor_run_dataset_client = last_succeeded_run_client.dataset()

    # Fetch items from the run's dataset
    dataset_items = actor_run_dataset_client.list_items().items
