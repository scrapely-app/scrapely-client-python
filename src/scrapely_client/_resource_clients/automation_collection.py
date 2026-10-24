# Scrapely-only resource (not part of the reference API).
# Copyright TeraShift GmbH. See the LICENSE and NOTICE files.
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from scrapely_client._docs import docs_group
from scrapely_client._resource_clients._resource_client import ResourceClient, ResourceClientAsync
from scrapely_client._utils.http import response_to_dict

if TYPE_CHECKING:
    from scrapely_client.types import Timeout


def _data(result: dict) -> dict:
    data = result.get('data', result)
    return data if isinstance(data, dict) else {}


@docs_group('Resource clients')
class AutomationCollectionClient(ResourceClient):
    """Sub-client for the automations in your account (Scrapely-only, `/v2/automations`).

    Plain schedules are automations too, so they are listed here as well. Responses are returned as plain
    dictionaries in the API's camelCase shape.
    """

    def __init__(
        self,
        *,
        resource_path: str = 'automations',
        **kwargs: Any,
    ) -> None:
        super().__init__(
            resource_path=resource_path,
            **kwargs,
        )

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        desc: bool | None = None,
        search: str | None = None,
        actor_id: str | None = None,
        saved_input_id: str | None = None,
        timeout: Timeout = 'medium',
    ) -> dict:
        """List automations.

        Args:
            limit: How many automations to retrieve.
            offset: How many automations to skip.
            desc: Whether to sort newest first (the default).
            search: Text to look for in the name or title.
            actor_id: Only automations where a step or the run-finished trigger uses this Actor.
            saved_input_id: Only automations where a step or the trigger uses this saved input (task).
            timeout: Timeout for the API HTTP request.

        Returns:
            A page with `total`, `count`, `offset`, `limit`, `desc` and `items`.
        """
        result = self._list(
            timeout=timeout,
            limit=limit,
            offset=offset,
            desc=desc,
            search=search,
            actorId=actor_id,
            savedInputId=saved_input_id,
        )
        return _data(result)

    def create(self, automation: dict[str, Any], *, timeout: Timeout = 'short') -> dict:
        """Create an automation.

        Args:
            automation: The automation (`trigger` and `steps` are required; `title`, `filters`, `ai`, `deliveries`
                and `options` are optional), in the API's camelCase shape.
            timeout: Timeout for the API HTTP request.

        Returns:
            The created automation.
        """
        response = self._http_client.call(
            url=self._build_url(),
            method='POST',
            params=self._build_params(),
            json=automation,
            timeout=timeout,
        )
        return _data(response_to_dict(response))


@docs_group('Resource clients')
class AutomationCollectionClientAsync(ResourceClientAsync):
    """Sub-client for the automations in your account (Scrapely-only, `/v2/automations`).

    Plain schedules are automations too, so they are listed here as well. Responses are returned as plain
    dictionaries in the API's camelCase shape.
    """

    def __init__(
        self,
        *,
        resource_path: str = 'automations',
        **kwargs: Any,
    ) -> None:
        super().__init__(
            resource_path=resource_path,
            **kwargs,
        )

    async def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        desc: bool | None = None,
        search: str | None = None,
        actor_id: str | None = None,
        saved_input_id: str | None = None,
        timeout: Timeout = 'medium',
    ) -> dict:
        """List automations.

        Args:
            limit: How many automations to retrieve.
            offset: How many automations to skip.
            desc: Whether to sort newest first (the default).
            search: Text to look for in the name or title.
            actor_id: Only automations where a step or the run-finished trigger uses this Actor.
            saved_input_id: Only automations where a step or the trigger uses this saved input (task).
            timeout: Timeout for the API HTTP request.

        Returns:
            A page with `total`, `count`, `offset`, `limit`, `desc` and `items`.
        """
        result = await self._list(
            timeout=timeout,
            limit=limit,
            offset=offset,
            desc=desc,
            search=search,
            actorId=actor_id,
            savedInputId=saved_input_id,
        )
        return _data(result)

    async def create(self, automation: dict[str, Any], *, timeout: Timeout = 'short') -> dict:
        """Create an automation.

        Args:
            automation: The automation (`trigger` and `steps` are required; `title`, `filters`, `ai`, `deliveries`
                and `options` are optional), in the API's camelCase shape.
            timeout: Timeout for the API HTTP request.

        Returns:
            The created automation.
        """
        response = await self._http_client.call(
            url=self._build_url(),
            method='POST',
            params=self._build_params(),
            json=automation,
            timeout=timeout,
        )
        return _data(response_to_dict(response))
