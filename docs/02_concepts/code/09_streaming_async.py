from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(TOKEN)
    run_client = scrapely_client.run('MY-RUN-ID')
    log_client = run_client.log()

    async with log_client.stream() as log_stream:
        if log_stream:
            async for bytes_chunk in log_stream.aiter_bytes():
                print(bytes_chunk)
