from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'


def main() -> None:
    scrapely_client = ScrapelyClient(TOKEN)
    rq_client = scrapely_client.request_queue('REQUEST-QUEUE-ID')

    # Plain dict — keys may be snake_case or camelCase.
    rq_client.add_request(
        {
            'url': 'https://example.com',
            'unique_key': 'https://example.com',
            'method': 'GET',
        }
    )
