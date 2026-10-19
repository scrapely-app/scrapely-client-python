import asyncio

from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(TOKEN)
    actor_client = scrapely_client.actor('my-actor-id')

    # Start the Actor and get the run ID
    run_result = await actor_client.start()
    run_client = scrapely_client.run(run_result.id)
    log_client = run_client.log()

    # Stream the logs
    async with log_client.stream() as async_log_stream:
        if async_log_stream:
            async for bytes_chunk in async_log_stream.aiter_bytes():
                print(bytes_chunk)


if __name__ == '__main__':
    asyncio.run(main())
