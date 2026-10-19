# Derived from apify-client-python (Copyright Apify Technologies s.r.o., Apache-2.0).
# Modified by TeraShift GmbH. See the LICENSE and NOTICE files.
from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager
from typing import TYPE_CHECKING, Any

from scrapely_client._docs import docs_group
from scrapely_client._resource_clients._resource_client import ResourceClient, ResourceClientAsync
from scrapely_client._utils.errors import catch_not_found_for_resource_or_throw
from scrapely_client.errors import ApifyApiError

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

    from scrapely_client.http_clients import HttpResponse
    from scrapely_client.types import Timeout


@docs_group('Resource clients')
class LogClient(ResourceClient):
    """Sub-client for managing a specific log.

    Provides methods to manage logs, e.g. get or stream them. Obtain an instance via an appropriate method on the
    `ScrapelyClient` class.
    """

    def __init__(
        self,
        *,
        resource_path: str = 'logs',
        **kwargs: Any,
    ) -> None:
        super().__init__(
            resource_path=resource_path,
            **kwargs,
        )

    def get(self, *, raw: bool = False, timeout: Timeout = 'long') -> str | None:
        """Retrieve the log as text.


        404s collapse to `None` only when this client targets a specific log by ID (e.g. `client.log(run_id).get()`).
        For chained clients without a `resource_id` (e.g. `run.log().get()`), a 404 is ambiguous and propagates.

        Args:
            raw: If true, the log will include formatting. For example, coloring character sequences.
            timeout: Timeout for the API HTTP request.

        Returns:
            The retrieved log, or None, if it does not exist.
        """
        try:
            response = self._http_client.call(
                url=self._build_url(),
                method='GET',
                params=self._build_params(raw=raw),
                timeout=timeout,
            )

            return response.text  # noqa: TRY300

        except ApifyApiError as exc:
            catch_not_found_for_resource_or_throw(exc, self._resource_id)

        return None

    def get_as_bytes(self, *, raw: bool = False, timeout: Timeout = 'long') -> bytes | None:
        """Retrieve the log as raw bytes.


        Args:
            raw: If true, the log will include formatting. For example, coloring character sequences.
            timeout: Timeout for the API HTTP request.

        Returns:
            The retrieved log as raw bytes, or None, if it does not exist.
        """
        try:
            response = self._http_client.call(
                url=self._build_url(),
                method='GET',
                params=self._build_params(raw=raw),
                timeout=timeout,
            )

            return response.content  # noqa: TRY300

        except ApifyApiError as exc:
            catch_not_found_for_resource_or_throw(exc, self._resource_id)

        return None

    @contextmanager
    def stream(self, *, raw: bool = False, timeout: Timeout = 'long') -> Iterator[HttpResponse | None]:
        """Retrieve the log as a stream.


        Args:
            raw: If true, the log will include formatting. For example, coloring character sequences.
            timeout: Timeout for the API HTTP request.

        Returns:
            The retrieved log as a context-managed streaming `Response`, or None, if it does not exist.
        """
        response = None
        try:
            response = self._http_client.call(
                url=self._build_url(),
                method='GET',
                params=self._build_params(stream=True, raw=raw),
                stream=True,
                timeout=timeout,
            )

            yield response
        except ApifyApiError as exc:
            catch_not_found_for_resource_or_throw(exc, self._resource_id)
            yield None
        finally:
            if response:
                response.close()


@docs_group('Resource clients')
class LogClientAsync(ResourceClientAsync):
    """Sub-client for managing a specific log.

    Provides methods to manage logs, e.g. get or stream them. Obtain an instance via an appropriate method on the
    `ScrapelyClientAsync` class.
    """

    def __init__(
        self,
        *,
        resource_path: str = 'logs',
        **kwargs: Any,
    ) -> None:
        super().__init__(
            resource_path=resource_path,
            **kwargs,
        )

    async def get(self, *, raw: bool = False, timeout: Timeout = 'long') -> str | None:
        """Retrieve the log as text.


        404s collapse to `None` only when this client targets a specific log by ID (e.g. `client.log(run_id).get()`).
        For chained clients without a `resource_id` (e.g. `run.log().get()`), a 404 is ambiguous and propagates.

        Args:
            raw: If true, the log will include formatting. For example, coloring character sequences.
            timeout: Timeout for the API HTTP request.

        Returns:
            The retrieved log, or None, if it does not exist.
        """
        try:
            response = await self._http_client.call(
                url=self._build_url(),
                method='GET',
                params=self._build_params(raw=raw),
                timeout=timeout,
            )

            return response.text  # noqa: TRY300

        except ApifyApiError as exc:
            catch_not_found_for_resource_or_throw(exc, self._resource_id)

        return None

    async def get_as_bytes(self, *, raw: bool = False, timeout: Timeout = 'long') -> bytes | None:
        """Retrieve the log as raw bytes.


        Args:
            raw: If true, the log will include formatting. For example, coloring character sequences.
            timeout: Timeout for the API HTTP request.

        Returns:
            The retrieved log as raw bytes, or None, if it does not exist.
        """
        try:
            response = await self._http_client.call(
                url=self._build_url(),
                method='GET',
                params=self._build_params(raw=raw),
                timeout=timeout,
            )

            return response.content  # noqa: TRY300

        except ApifyApiError as exc:
            catch_not_found_for_resource_or_throw(exc, self._resource_id)

        return None

    @asynccontextmanager
    async def stream(self, *, raw: bool = False, timeout: Timeout = 'long') -> AsyncIterator[HttpResponse | None]:
        """Retrieve the log as a stream.


        Args:
            raw: If true, the log will include formatting. For example, coloring character sequences.
            timeout: Timeout for the API HTTP request.

        Returns:
            The retrieved log as a context-managed streaming `Response`, or None, if it does not exist.
        """
        response = None
        try:
            response = await self._http_client.call(
                url=self._build_url(),
                method='GET',
                params=self._build_params(stream=True, raw=raw),
                stream=True,
                timeout=timeout,
            )

            yield response
        except ApifyApiError as exc:
            catch_not_found_for_resource_or_throw(exc, self._resource_id)
            yield None
        finally:
            if response:
                await response.aclose()
