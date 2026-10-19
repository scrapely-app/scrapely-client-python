# Derived from apify-client-python (Copyright Apify Technologies s.r.o., Apache-2.0).
# Modified by TeraShift GmbH. See the LICENSE and NOTICE files.
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from scrapely_client._docs import docs_group
from scrapely_client._models import ListOfActorsInStoreResponse, ListOfStoreActors
from scrapely_client._pagination import get_items_iterator, get_items_iterator_async
from scrapely_client._resource_clients._resource_client import ResourceClient, ResourceClientAsync

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

    from scrapely_client._models import StoreListActor
    from scrapely_client.types import Timeout


@docs_group('Resource clients')
class StoreCollectionClient(ResourceClient):
    """Sub-client for the Scrapely store collection.

    Provides methods to browse the Scrapely store, e.g. list available Actors. Obtain an instance via an appropriate
    method on the `ScrapelyClient` class.
    """

    def __init__(
        self,
        *,
        resource_path: str = 'store/actors',  # Scrapely mounts the store listing at /v2/store/actors
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
        search: str | None = None,
        sort_by: str | None = None,
        category: str | None = None,
        username: str | None = None,
        pricing_model: str | None = None,
        include_unrunnable_actors: bool | None = None,
        timeout: Timeout = 'medium',
    ) -> ListOfStoreActors:
        """List Actors in Scrapely store.


        Args:
            limit: How many Actors to list.
            offset: What Actor to include as first when retrieving the list.
            search: String to search by. The search runs on the following fields: title, name, description, username,
                readme.
            sort_by: Specifies the field by which to sort the results.
            category: Filter by this category.
            username: Filter by this username.
            pricing_model: Filter by this pricing model.
            include_unrunnable_actors: If True, the response will include Actors that cannot be run.
            timeout: Timeout for the API HTTP request.

        Returns:
            The list of available Actors matching the specified filters.
        """
        result = self._list(
            timeout=timeout,
            limit=limit,
            offset=offset,
            search=search,
            sortBy=sort_by,
            category=category,
            username=username,
            pricingModel=pricing_model,
            includeUnrunnableActors=include_unrunnable_actors,
        )
        return ListOfActorsInStoreResponse.model_validate(result).data

    def iterate(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        sort_by: str | None = None,
        category: str | None = None,
        username: str | None = None,
        pricing_model: str | None = None,
        include_unrunnable_actors: bool | None = None,
        timeout: Timeout = 'medium',
    ) -> Iterator[StoreListActor]:
        """Iterate over Actors in Scrapely store.

        Simple `list` does only one API call, possibly not listing all items matching the criteria. This method
        returns an iterator that is capable of making multiple API calls to retrieve all items matching the criteria.


        Args:
            limit: How many Actors to list.
            offset: What Actor to include as first when retrieving the list.
            search: String to search by. The search runs on the following fields: title, name, description, username,
                readme.
            sort_by: Specifies the field by which to sort the results.
            category: Filter by this category.
            username: Filter by this username.
            pricing_model: Filter by this pricing model.
            include_unrunnable_actors: If True, the response will include Actors that cannot be run.
            timeout: Timeout for the API HTTP request.

        Yields:
            The Actors in the store matching the specified filters.
        """

        def _callback(*, limit: int | None = None, offset: int | None = None) -> ListOfStoreActors:
            return self.list(
                limit=limit,
                offset=offset,
                search=search,
                sort_by=sort_by,
                category=category,
                username=username,
                pricing_model=pricing_model,
                include_unrunnable_actors=include_unrunnable_actors,
                timeout=timeout,
            )

        return get_items_iterator(_callback, limit=limit, offset=offset)


@docs_group('Resource clients')
class StoreCollectionClientAsync(ResourceClientAsync):
    """Sub-client for the Scrapely store collection.

    Provides methods to browse the Scrapely store, e.g. list available Actors. Obtain an instance via an appropriate
    method on the `ScrapelyClientAsync` class.
    """

    def __init__(
        self,
        *,
        resource_path: str = 'store/actors',  # Scrapely mounts the store listing at /v2/store/actors
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
        search: str | None = None,
        sort_by: str | None = None,
        category: str | None = None,
        username: str | None = None,
        pricing_model: str | None = None,
        include_unrunnable_actors: bool | None = None,
        timeout: Timeout = 'medium',
    ) -> ListOfStoreActors:
        """List Actors in Scrapely store.


        Args:
            limit: How many Actors to list.
            offset: What Actor to include as first when retrieving the list.
            search: String to search by. The search runs on the following fields: title, name, description, username,
                readme.
            sort_by: Specifies the field by which to sort the results.
            category: Filter by this category.
            username: Filter by this username.
            pricing_model: Filter by this pricing model.
            include_unrunnable_actors: If True, the response will include Actors that cannot be run.
            timeout: Timeout for the API HTTP request.

        Returns:
            The list of available Actors matching the specified filters.
        """
        result = await self._list(
            timeout=timeout,
            limit=limit,
            offset=offset,
            search=search,
            sortBy=sort_by,
            category=category,
            username=username,
            pricingModel=pricing_model,
            includeUnrunnableActors=include_unrunnable_actors,
        )
        return ListOfActorsInStoreResponse.model_validate(result).data

    def iterate(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        search: str | None = None,
        sort_by: str | None = None,
        category: str | None = None,
        username: str | None = None,
        pricing_model: str | None = None,
        include_unrunnable_actors: bool | None = None,
        timeout: Timeout = 'medium',
    ) -> AsyncIterator[StoreListActor]:
        """Iterate over Actors in Scrapely store.

        Simple `list` does only one API call, possibly not listing all items matching the criteria. This method
        returns an iterator that is capable of making multiple API calls to retrieve all items matching the criteria.


        Args:
            limit: How many Actors to list.
            offset: What Actor to include as first when retrieving the list.
            search: String to search by. The search runs on the following fields: title, name, description, username,
                readme.
            sort_by: Specifies the field by which to sort the results.
            category: Filter by this category.
            username: Filter by this username.
            pricing_model: Filter by this pricing model.
            include_unrunnable_actors: If True, the response will include Actors that cannot be run.
            timeout: Timeout for the API HTTP request.

        Yields:
            The Actors in the store matching the specified filters.
        """

        async def _callback(*, limit: int | None = None, offset: int | None = None) -> ListOfStoreActors:
            return await self.list(
                limit=limit,
                offset=offset,
                search=search,
                sort_by=sort_by,
                category=category,
                username=username,
                pricing_model=pricing_model,
                include_unrunnable_actors=include_unrunnable_actors,
                timeout=timeout,
            )

        return get_items_iterator_async(_callback, limit=limit, offset=offset)
