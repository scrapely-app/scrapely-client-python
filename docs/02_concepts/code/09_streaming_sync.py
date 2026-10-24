# Derived from apify-client-python (docs/02_concepts/code/09_streaming_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)
    run_client = scrapely_client.run('MY-RUN-ID')
    log_client = run_client.log()

    with log_client.stream() as log_stream:
        if log_stream:
            for bytes_chunk in log_stream.iter_bytes():
                print(bytes_chunk)
