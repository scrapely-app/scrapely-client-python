# Scrapely-only resource (not part of the reference API).
# Copyright TeraShift GmbH. See the LICENSE and NOTICE files.
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from scrapely_client._docs import docs_group
from scrapely_client._resource_clients._resource_client import ResourceClient, ResourceClientAsync
from scrapely_client._utils.errors import catch_not_found_or_throw
from scrapely_client._utils.http import response_to_dict, to_path_segment
from scrapely_client.errors import ApifyApiError

if TYPE_CHECKING:
    from scrapely_client.types import Timeout


def _data(result: dict) -> dict:
    data = result.get('data', result)
    return data if isinstance(data, dict) else {}


@docs_group('Resource clients')
class AutomationClient(ResourceClient):
    """Sub-client for a specific automation (Scrapely-only, `/v2/automations/:id`).

    An automation is one trigger (manual, schedule or another run finished), run steps (an Actor with input, or a
    saved input with an optional override), optional filters, an optional AI step and deliveries. Responses are
    returned as plain dictionaries in the API's camelCase shape.
    """

    def __init__(
        self,
        *,
        resource_id: str,
        resource_path: str = 'automations',
        **kwargs: Any,
    ) -> None:
        super().__init__(
            resource_id=resource_id,
            resource_path=resource_path,
            **kwargs,
        )

    def get(self, *, timeout: Timeout = 'short') -> dict | None:
        """Return the automation.

        Args:
            timeout: Timeout for the API HTTP request.

        Returns:
            The automation, or None if it does not exist.
        """
        result = self._get(timeout=timeout)
        if result is None:
            return None
        return _data(result)

    def update(self, fields: dict[str, Any], *, timeout: Timeout = 'short') -> dict:
        """Update the automation. Only the given parts change.

        Fields are sent as given, so `{'ai': None}` removes the AI step. A delivery sent back with its `id` and no new
        secret keeps the stored secret.

        Args:
            fields: Parts to change (`title`, `trigger`, `steps`, `filters`, `ai`, `deliveries`, `options`, ...).
            timeout: Timeout for the API HTTP request.

        Returns:
            The updated automation.
        """
        response = self._http_client.call(
            url=self._build_url(),
            method='PUT',
            params=self._build_params(),
            json=fields,
            timeout=timeout,
        )
        return _data(response_to_dict(response))

    def delete(self, *, timeout: Timeout = 'short') -> None:
        """Delete the automation and its run history.

        Args:
            timeout: Timeout for the API HTTP request.
        """
        self._delete(timeout=timeout)

    def run(self, *, timeout: Timeout = 'medium') -> dict:
        """Run the automation now, whatever its trigger.

        Args:
            timeout: Timeout for the API HTTP request.

        Returns:
            The new automation run.
        """
        response = self._http_client.call(
            url=self._build_url('runs'),
            method='POST',
            params=self._build_params(),
            timeout=timeout,
        )
        return _data(response_to_dict(response))

    def list_runs(self, *, limit: int | None = None, offset: int | None = None, timeout: Timeout = 'medium') -> dict:
        """List the automation's runs, newest first (the last 30 are kept).

        Args:
            limit: How many runs to retrieve (at most 100).
            offset: How many runs to skip.
            timeout: Timeout for the API HTTP request.

        Returns:
            A page with `total`, `count`, `offset`, `limit` and `items`.
        """
        response = self._http_client.call(
            url=self._build_url('runs'),
            method='GET',
            params=self._build_params(limit=limit, offset=offset),
            timeout=timeout,
        )
        return _data(response_to_dict(response))

    def get_run(self, run_id: str, *, timeout: Timeout = 'short') -> dict | None:
        """Return one run of the automation (steps, filter result, AI output and cost, deliveries).

        Args:
            run_id: ID of the automation run.
            timeout: Timeout for the API HTTP request.

        Returns:
            The run, or None if it does not exist.
        """
        try:
            response = self._http_client.call(
                url=self._build_url(f'runs/{to_path_segment(run_id)}'),
                method='GET',
                params=self._build_params(),
                timeout=timeout,
            )
        except ApifyApiError as exc:
            catch_not_found_or_throw(exc)
            return None
        return _data(response_to_dict(response))

    def duplicate(
        self,
        *,
        title: str | None = None,
        name: str | None = None,
        is_enabled: bool | None = None,
        timeout: Timeout = 'short',
    ) -> dict:
        """Create a copy of the automation. Stored delivery secrets are copied on the server.

        Args:
            title: Title of the copy (default: the original title with "(copy)").
            name: API name of the copy (default: generated).
            is_enabled: Whether the copy is enabled; it is paused unless this is True.
            timeout: Timeout for the API HTTP request.

        Returns:
            The new automation.
        """
        body = {k: v for k, v in {'title': title, 'name': name, 'isEnabled': is_enabled}.items() if v is not None}
        response = self._http_client.call(
            url=self._build_url('duplicate'),
            method='POST',
            params=self._build_params(),
            json=body,
            timeout=timeout,
        )
        return _data(response_to_dict(response))


@docs_group('Resource clients')
class AutomationClientAsync(ResourceClientAsync):
    """Sub-client for a specific automation (Scrapely-only, `/v2/automations/:id`).

    An automation is one trigger (manual, schedule or another run finished), run steps (an Actor with input, or a
    saved input with an optional override), optional filters, an optional AI step and deliveries. Responses are
    returned as plain dictionaries in the API's camelCase shape.
    """

    def __init__(
        self,
        *,
        resource_id: str,
        resource_path: str = 'automations',
        **kwargs: Any,
    ) -> None:
        super().__init__(
            resource_id=resource_id,
            resource_path=resource_path,
            **kwargs,
        )

    async def get(self, *, timeout: Timeout = 'short') -> dict | None:
        """Return the automation.

        Args:
            timeout: Timeout for the API HTTP request.

        Returns:
            The automation, or None if it does not exist.
        """
        result = await self._get(timeout=timeout)
        if result is None:
            return None
        return _data(result)

    async def update(self, fields: dict[str, Any], *, timeout: Timeout = 'short') -> dict:
        """Update the automation. Only the given parts change.

        Fields are sent as given, so `{'ai': None}` removes the AI step. A delivery sent back with its `id` and no new
        secret keeps the stored secret.

        Args:
            fields: Parts to change (`title`, `trigger`, `steps`, `filters`, `ai`, `deliveries`, `options`, ...).
            timeout: Timeout for the API HTTP request.

        Returns:
            The updated automation.
        """
        response = await self._http_client.call(
            url=self._build_url(),
            method='PUT',
            params=self._build_params(),
            json=fields,
            timeout=timeout,
        )
        return _data(response_to_dict(response))

    async def delete(self, *, timeout: Timeout = 'short') -> None:
        """Delete the automation and its run history.

        Args:
            timeout: Timeout for the API HTTP request.
        """
        await self._delete(timeout=timeout)

    async def run(self, *, timeout: Timeout = 'medium') -> dict:
        """Run the automation now, whatever its trigger.

        Args:
            timeout: Timeout for the API HTTP request.

        Returns:
            The new automation run.
        """
        response = await self._http_client.call(
            url=self._build_url('runs'),
            method='POST',
            params=self._build_params(),
            timeout=timeout,
        )
        return _data(response_to_dict(response))

    async def list_runs(
        self, *, limit: int | None = None, offset: int | None = None, timeout: Timeout = 'medium'
    ) -> dict:
        """List the automation's runs, newest first (the last 30 are kept).

        Args:
            limit: How many runs to retrieve (at most 100).
            offset: How many runs to skip.
            timeout: Timeout for the API HTTP request.

        Returns:
            A page with `total`, `count`, `offset`, `limit` and `items`.
        """
        response = await self._http_client.call(
            url=self._build_url('runs'),
            method='GET',
            params=self._build_params(limit=limit, offset=offset),
            timeout=timeout,
        )
        return _data(response_to_dict(response))

    async def get_run(self, run_id: str, *, timeout: Timeout = 'short') -> dict | None:
        """Return one run of the automation (steps, filter result, AI output and cost, deliveries).

        Args:
            run_id: ID of the automation run.
            timeout: Timeout for the API HTTP request.

        Returns:
            The run, or None if it does not exist.
        """
        try:
            response = await self._http_client.call(
                url=self._build_url(f'runs/{to_path_segment(run_id)}'),
                method='GET',
                params=self._build_params(),
                timeout=timeout,
            )
        except ApifyApiError as exc:
            catch_not_found_or_throw(exc)
            return None
        return _data(response_to_dict(response))

    async def duplicate(
        self,
        *,
        title: str | None = None,
        name: str | None = None,
        is_enabled: bool | None = None,
        timeout: Timeout = 'short',
    ) -> dict:
        """Create a copy of the automation. Stored delivery secrets are copied on the server.

        Args:
            title: Title of the copy (default: the original title with "(copy)").
            name: API name of the copy (default: generated).
            is_enabled: Whether the copy is enabled; it is paused unless this is True.
            timeout: Timeout for the API HTTP request.

        Returns:
            The new automation.
        """
        body = {k: v for k, v in {'title': title, 'name': name, 'isEnabled': is_enabled}.items() if v is not None}
        response = await self._http_client.call(
            url=self._build_url('duplicate'),
            method='POST',
            params=self._build_params(),
            json=body,
            timeout=timeout,
        )
        return _data(response_to_dict(response))
