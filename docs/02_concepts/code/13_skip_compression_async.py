import asyncio
from pathlib import Path

from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(TOKEN)
    kvs_client = scrapely_client.key_value_store('MY-KVS-ID')

    screenshot = await asyncio.to_thread(Path('screenshot.png').read_bytes)

    # The explicit content type lets the client skip compressing the PNG.
    await kvs_client.set_record('screenshot', screenshot, content_type='image/png')


if __name__ == '__main__':
    asyncio.run(main())
