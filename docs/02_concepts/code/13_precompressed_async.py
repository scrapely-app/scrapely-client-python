# Derived from apify-client-python (docs/02_concepts/code/13_precompressed_async.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
import asyncio
import gzip
from pathlib import Path

from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(TOKEN)
    kvs_client = scrapely_client.key_value_store('MY-KVS-ID')

    report = await asyncio.to_thread(Path('report.csv').read_bytes)
    compressed_report = await asyncio.to_thread(gzip.compress, report)

    # The explicit content encoding stops the client from compressing the bytes again.
    await kvs_client.set_record(
        'report',
        compressed_report,
        content_type='text/csv',
        content_encoding='gzip',
    )


if __name__ == '__main__':
    asyncio.run(main())
