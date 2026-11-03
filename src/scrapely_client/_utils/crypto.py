# Derived from apify-client-python (Copyright Apify Technologies s.r.o., Apache-2.0).
# Modified by TeraShift GmbH. See the LICENSE and NOTICE files.
from __future__ import annotations

import hashlib
import hmac
import string
import time
from base64 import urlsafe_b64encode
from datetime import timedelta
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit

from scrapely_client._utils.time import to_seconds

_BASE62_CHARSET = string.digits + string.ascii_letters

STORAGE_SIGNATURE_VERSION = 2
"""Version of newly minted storage signatures (binds method, path, record key and query string)."""

DEFAULT_STORAGE_URL_EXPIRES_IN = timedelta(hours=1)
"""Validity of a storage signature when the caller does not set `expires_in`."""


def encode_base62(num: int) -> str:
    """Encode an integer to a base62 string.

    Args:
        num: The number to encode.

    Returns:
        The base62-encoded string.
    """
    if num == 0:
        return _BASE62_CHARSET[0]

    # Use list to build result for O(n) complexity instead of O(n^2) string concatenation.
    parts = []
    while num > 0:
        num, remainder = divmod(num, 62)
        parts.append(_BASE62_CHARSET[remainder])

    # Reverse and join once at the end.
    return ''.join(reversed(parts))


def create_hmac_signature(secret_key: str, message: str) -> str:
    """Generate an HMAC-SHA256 signature and encode it using base62.

    The HMAC signature is truncated to 30 characters and then encoded in base62 to reduce the signature length.

    Args:
        secret_key: The secret key used for signing.
        message: The message to be signed.

    Returns:
        The base62-encoded signature.
    """
    signature = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()[:30]

    decimal_signature = int(signature, 16)

    return encode_base62(decimal_signature)


def storage_signature_query(url: str) -> str:
    """Return the canonical query string a version 2 storage signature binds.

    The raw query of `url` is parsed like `URLSearchParams` (`+` is a space), `signature` is dropped, each key and
    value is percent-encoded (RFC 3986: only `A-Z a-z 0-9 - . _ ~` stay as is), and the pairs are sorted by encoded
    key, then encoded value, and joined as `k=v&k=v`. The Scrapely API and the JS client build the same string.

    Args:
        url: The URL (or path with a query string) to canonicalize.

    Returns:
        The canonical query string, empty when the URL has no other parameters.
    """
    pairs = sorted(
        (quote(key, safe=''), quote(value, safe=''))
        for key, value in parse_qsl(urlsplit(url).query, keep_blank_values=True)
        if key != 'signature'
    )
    return '&'.join(f'{key}={value}' for key, value in pairs)


def create_storage_content_signature(
    resource_id: str,
    url_signing_secret_key: str,
    *,
    method: str,
    path: str,
    record_key: str | None = None,
    query: str = '',
    expires_in: timedelta | None = None,
) -> str:
    """Create a signature for a storage resource URL like dataset items or a key-value store record.

    The signature binds the HTTP method, the URL path, the canonical query string (`storage_signature_query`) and,
    for a single record, the record key, so the API refuses it for any other request. The signed message is
    `{version}.{expires_at}.{resource_id}.{METHOD}.{path}.{record_key}.{query}`, the same as the Scrapely API and the
    JS client.

    Args:
        resource_id: The unique identifier of the storage resource.
        url_signing_secret_key: The secret key for signing the URL.
        method: The HTTP method the signature authorizes, e.g. `GET`.
        path: The URL path (no query string), beginning with `/`.
        record_key: The record key when the signature authorizes exactly one record.
        query: The canonical query string from `storage_signature_query`.
        expires_in: How long the signature is valid. Defaults to 1 hour; it cannot be non-expiring.

    Returns:
        The base64url-encoded signature string.
    """
    expires_in_secs = to_seconds(expires_in if expires_in is not None else DEFAULT_STORAGE_URL_EXPIRES_IN)
    if expires_in_secs <= 0:
        raise ValueError('expires_in must be a positive duration')
    expires_at = int(time.time() * 1000) + round(expires_in_secs * 1000)
    version = STORAGE_SIGNATURE_VERSION

    message_to_sign = f'{version}.{expires_at}.{resource_id}.{method.upper()}.{path}.{record_key or ""}.{query}'
    hmac_sig = create_hmac_signature(url_signing_secret_key, message_to_sign)

    # Unpadded, like the JS client and Node's base64url.
    return urlsafe_b64encode(f'{version}.{expires_at}.{hmac_sig}'.encode()).decode('utf-8').rstrip('=')


def sign_storage_url(
    url: str,
    resource_id: str,
    url_signing_secret_key: str,
    *,
    method: str = 'GET',
    record_key: str | None = None,
    expires_in: timedelta | None = None,
) -> str:
    """Append a `signature` parameter that binds the URL's path and query string.

    Args:
        url: The finished URL, with every other query parameter already set.
        resource_id: The unique identifier of the storage resource.
        url_signing_secret_key: The secret key for signing the URL.
        method: The HTTP method the signature authorizes.
        record_key: The record key when the URL is for exactly one record.
        expires_in: How long the signature is valid. Defaults to 1 hour.

    Returns:
        The URL with the signature appended.
    """
    parts = urlsplit(url)
    signature = create_storage_content_signature(
        resource_id,
        url_signing_secret_key,
        method=method,
        path=parts.path,
        record_key=record_key,
        query=storage_signature_query(url),
        expires_in=expires_in,
    )
    signature_param = urlencode({'signature': signature})
    return urlunsplit(parts._replace(query=f'{parts.query}&{signature_param}' if parts.query else signature_param))
