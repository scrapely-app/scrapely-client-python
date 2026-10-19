from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(TOKEN)
    rq_client = scrapely_client.request_queue('REQUEST-QUEUE-ID')

    # Plain dict — keys may be snake_case or camelCase.
    await rq_client.add_request(
        {
            'url': 'https://example.com',
            'unique_key': 'https://example.com',
            'method': 'GET',
        }
    )
