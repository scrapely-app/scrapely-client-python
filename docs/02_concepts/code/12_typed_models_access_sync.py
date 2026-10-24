# Derived from apify-client-python (docs/02_concepts/code/12_typed_models_access_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)

    # `get` returns an `Actor` Pydantic model — fields are typed and IDE-completable.
    actor = scrapely_client.actor('my-user/hello-world').get()
    if actor is None:
        return

    print(actor.id)  # str
    print(actor.username)  # str
    print(actor.is_public)  # bool
    print(actor.created_at)  # datetime.datetime (timezone-aware)
    print(actor.stats.total_runs)  # int — nested model, attribute access all the way down
