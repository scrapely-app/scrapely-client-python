# Derived from apify-client-python (Copyright Apify Technologies s.r.o., Apache-2.0).
# Modified by TeraShift GmbH. See the LICENSE and NOTICE files.
from importlib import metadata

from ._charging import (
    USES_PUSH_DATA_INTERCEPTION,
    ChargeResult,
    ChargingHooks,
    PpeAwarePushDataContext,
    normalize_items,
    push_data_charging_context,
)
from ._scrapely_client import ApifyClient, ApifyClientAsync, ScrapelyClient, ScrapelyClientAsync

try:
    __version__ = metadata.version('scrapely-client-python')
except metadata.PackageNotFoundError:
    __version__ = '0.0.0'

__all__ = [
    'USES_PUSH_DATA_INTERCEPTION',
    'ApifyClient',
    'ApifyClientAsync',
    'ChargeResult',
    'ChargingHooks',
    'PpeAwarePushDataContext',
    'ScrapelyClient',
    'ScrapelyClientAsync',
    '__version__',
    'normalize_items',
    'push_data_charging_context',
]
