"""Opt-in pay-per-event charging interception for dataset pushes.

Charging interception for dataset pushes, implemented in the client
itself, with the charging logic supplied by the host SDK via the
:class:`ChargingHooks` protocol (no SDK import — the SDK adapts its
``ChargingManager`` to these hooks later).

Without hooks (the default), dataset pushes are not intercepted.
"""

from __future__ import annotations

import inspect
import json
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Protocol, cast, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Sequence

USES_PUSH_DATA_INTERCEPTION = '__scrapely_uses_push_data_interception__'
"""Attribute marking dataset clients whose ``push_items`` charges pay-per-event items.

The host SDK checks this attribute to detect that push-data interception is active."""


@dataclass(frozen=True)
class ChargeResult:
    """Result of a charged push-data operation.

    Mirrors the SDK-side ``ChargeResult`` contract; the client only stores and merges
    these values, it never computes them.
    """

    event_charge_limit_reached: bool
    """Whether an event charge limit was reached during the operation."""

    charged_count: int
    """Total number of charged items."""

    chargeable_within_limit: dict[str, int | None] = field(default_factory=dict)
    """How many more items could be charged per event within the current limits."""


@dataclass
class PpeAwarePushDataContext:
    """Context carried through ``push_data_charging_context``.

    Wrapping a push in ``push_data_charging_context.run({...}, fn)`` makes every
    intercepted ``push_items()`` inside ``fn`` charge ``event_name`` and merge its
    result into the context.
    """

    event_name: str | None = None
    charge_result: ChargeResult | None = None


push_data_charging_context: ContextVar[PpeAwarePushDataContext | None] = ContextVar(
    'scrapely_push_data_charging_context', default=None
)
"""ContextVar for the current :class:`PpeAwarePushDataContext` (async-local in asyncio)."""


@runtime_checkable
class ChargingHooks(Protocol):
    """Charging hooks supplied by the host SDK (e.g. ``scrapely``'s ``ChargingManager``).

    The client knows nothing about pricing, budgets or ledgers — it only routes
    ``push_items()`` through these hooks when they are configured and the dataset
    is the actor run's default dataset.
    """

    def should_charge_dataset_pushes(self, dataset_id: str) -> bool:
        """Whether pushes to this dataset should be intercepted and charged."""
        ...

    def push_and_charge(
        self,
        *,
        items: Sequence[dict[str, Any]],
        event_name: str | None,
        push_fn: Callable[[Sequence[dict[str, Any]]], Any],
    ) -> ChargeResult | Awaitable[ChargeResult]:
        """Charge for (and persist) the given items.

        ``push_fn`` persists the budget-limited subset of items; implementations must
        call it with only the items that were actually accepted for charging. Both
        sync and async implementations are supported (async clients await awaitables).
        """
        ...

    def merge_charge_results(self, a: ChargeResult, b: ChargeResult) -> ChargeResult:
        """Merge two charge results (e.g. multiple pushes within one context)."""
        ...


def normalize_items(items: Any) -> list[dict[str, Any]]:
    """Normalize ``push_items`` input (str, dict, or list of either) to a list of dicts."""
    if isinstance(items, str):
        parsed = json.loads(items)
        return parsed if isinstance(parsed, list) else [parsed]
    if isinstance(items, list):
        result: list[dict[str, Any]] = []
        for item in items:
            if isinstance(item, str):
                parsed = json.loads(item)
                if isinstance(parsed, list):
                    result.extend(parsed)
                else:
                    result.append(parsed)
            else:
                result.append(item)
        return result
    return [items]


def _merge_context_charge_result(context: PpeAwarePushDataContext, hooks: ChargingHooks, result: ChargeResult) -> None:
    if context.charge_result is None:
        context.charge_result = result
    else:
        context.charge_result = hooks.merge_charge_results(context.charge_result, result)


def wrap_dataset_client_with_charging(client: Any, hooks: ChargingHooks, *, is_async: bool) -> Any:
    """Wrap a dataset client's ``push_items`` with charging interception (method swap by design).

    Normalize items →
    ``push_and_charge`` with a ``push_fn`` that pushes the accepted subset via the
    original ``push_items``, and accumulate the charge result into the ambient
    ``push_data_charging_context`` when present.
    """
    original_push_items = client.push_items

    if is_async:

        async def patched_push_items(items: Any, **kwargs: Any) -> None:
            context = push_data_charging_context.get()
            normalized = normalize_items(items)

            async def push_fn(limited_items: Sequence[dict[str, Any]]) -> None:
                await original_push_items(limited_items, **kwargs)

            outcome = hooks.push_and_charge(
                items=normalized, event_name=context.event_name if context else None, push_fn=push_fn
            )
            if inspect.isawaitable(outcome):
                outcome = await outcome
            result = cast('ChargeResult', outcome)
            if context is not None:
                _merge_context_charge_result(context, hooks, result)

    else:

        def patched_push_items(items: Any, **kwargs: Any) -> None:
            context = push_data_charging_context.get()
            normalized = normalize_items(items)

            def push_fn(limited_items: Sequence[dict[str, Any]]) -> None:
                original_push_items(limited_items, **kwargs)

            outcome = hooks.push_and_charge(
                items=normalized, event_name=context.event_name if context else None, push_fn=push_fn
            )
            result = cast('ChargeResult', outcome)
            if inspect.isawaitable(outcome):
                msg = 'Sync clients require synchronous ChargingHooks.push_and_charge'
                raise TypeError(msg)
            if context is not None:
                _merge_context_charge_result(context, hooks, result)

    client.push_items = patched_push_items  # type: ignore[method-assign]
    setattr(client, USES_PUSH_DATA_INTERCEPTION, True)
    return client


__all__ = [
    'USES_PUSH_DATA_INTERCEPTION',
    'ChargeResult',
    'ChargingHooks',
    'PpeAwarePushDataContext',
    'normalize_items',
    'push_data_charging_context',
    'wrap_dataset_client_with_charging',
]
