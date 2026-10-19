from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(TOKEN)

    # `get` returns an `Actor` Pydantic model — fields are typed and IDE-completable.
    actor = await scrapely_client.actor('my-user/hello-world').get()
    if actor is None:
        return

    print(actor.id)  # str
    print(actor.username)  # str
    print(actor.is_public)  # bool
    print(actor.created_at)  # datetime.datetime (timezone-aware)
    print(actor.stats.total_runs)  # int — nested model, attribute access all the way down
