# Derived from apify-client-python (docs/02_concepts/code/10_plugging_in_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from typing import Any

from scrapely_client import ScrapelyClient
from scrapely_client.http_clients import HttpClient, HttpResponse
from scrapely_client.types import Timeout

TOKEN = 'MY-SCRAPELY-TOKEN'


class MyHttpClient(HttpClient):
    """Custom sync HTTP client."""

    def call(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: str | bytes | bytearray | None = None,
        json: Any = None,
        stream: bool | None = None,
        timeout: Timeout = 'medium',
    ) -> HttpResponse: ...


def main() -> None:
    client = ScrapelyClient.with_custom_http_client(
        token=TOKEN,
        http_client=MyHttpClient(),
    )
