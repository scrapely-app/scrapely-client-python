# Scrape.ly addition (TeraShift GmbH): "out of credit" data of the API.
"""Read the unlock data of an "out of credit" answer and warn about held results.

When the account's free credit runs out, the API answers run starts (and other paid requests) with HTTP 402 and puts
the way out in `error.data` (`ApifyApiError.data`): `unlock` (the Starter offer and its `checkoutUrl`) for a Free
account, `topUpUrl` for a paid one, and the account's newest held run (`heldItems`, `heldUntil`, `runId`). A run
that went on finding results after the credit ran out has `held` (`RunHeld`): the results are kept out of its
dataset until the account unlocks them.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from scrapely_client._logging import logger

if TYPE_CHECKING:
    from scrapely_client._models import Run

CREDIT_REASONS = frozenset({'insufficient-credit', 'insufficient-funds'})
PAYMENT_REQUIRED_STATUS = 402


def is_insufficient_credit_error(err: BaseException | Any) -> bool:
    """Whether `err` is the API's HTTP 402 for the account balance (its unlock data is in `err.data`)."""
    data = getattr(err, 'data', None)
    return (
        getattr(err, 'status_code', None) == PAYMENT_REQUIRED_STATUS
        and isinstance(data, dict)
        and data.get('reason') in CREDIT_REASONS
    )


def credit_unlock_url(err: BaseException | Any) -> str | None:
    """Return the link to show the user for a 402 for the balance: the unlock checkout, else the top-up page."""
    if not is_insufficient_credit_error(err):
        return None
    data = getattr(err, 'data', None) or {}
    unlock = data.get('unlock')
    url = unlock.get('checkoutUrl') if isinstance(unlock, dict) else None
    url = url or data.get('topUpUrl')
    return url if isinstance(url, str) and url else None


def held_run_warning(run: Run | None) -> str | None:
    """Return one warning line for a run with held results that can still be unlocked, else None."""
    if run is None:
        return None
    held = run.held
    n = held.items if held is not None else None
    if held is None or not n or n <= 0 or held.status not in ('holding', 'held'):
        return None
    until = f' until {held.held_until.isoformat().replace("+00:00", "Z")}' if held.held_until else ''
    checkout_url = held.unlock.checkout_url if held.unlock is not None else None
    link = f' Unlock them: {checkout_url}' if checkout_url else ''
    noun = 'result is' if n == 1 else 'results are'
    return f'Run {run.id}: your free credit ran out, so {n:,} more {noun} held{until}.{link}'


def warn_if_held(run: Run | None) -> None:
    """Log `held_run_warning(run)` when there is one."""
    warning = held_run_warning(run)
    if warning:
        logger.warning(warning)
