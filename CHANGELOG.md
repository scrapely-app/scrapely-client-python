# Changelog

All notable changes to this project will be documented in this file.

## [1.0.9] - 2026-10-24

- The `SCRAPELY_API_URL` environment variable sets the API URL when `api_url` is not passed to `ScrapelyClient`, `ScrapelyClientAsync` or `with_custom_http_client`; `api_url` still wins, and without either the client uses `https://api.scrape.ly`. An empty value is ignored. `api_public_url` is unchanged.
- Version 1.0.3 defaulted to `https://api-staging.scrape.ly`; upgrade to 1.0.6 or later.

## [1.0.8] - 2026-10-20

- Request ids are percent-encoded as one URL path segment in `get_request`, `update_request`, `delete_request`, `prolong_request_lock` and `delete_request_lock` (sync and async); `''`, `.` and `..` raise `ValueError`. `update_request` checks the id against the API's grammar (1-128 letters, digits, `-`, `_`, `~`) and refuses a request without an id instead of sending `requests/None`. Resource ids (`client.dataset(id)`, versions, env vars) and automation run ids are encoded the same way. An id such as `..` used to send the call to another resource.
- Models are generated from a committed, hash-checked copy of the OpenAPI specification; model docstrings updated, no behaviour change.

## [1.0.7] - 2026-10-20

- Maintenance release.

## [1.0.6] - 2026-10-20

- New Scrapely-only `client.automations()` (`list` with `actor_id`, `saved_input_id` and `search` filters, `create`) and `client.automation(id)` (`get`, `update`, `delete`, `run`, `list_runs`, `get_run`, `duplicate`) for `/v2/automations`, sync and async. They return the API's camelCase dictionaries; `update` sends fields as given, so `{'ai': None}` removes the AI step.

## [1.0.5] - 2026-10-20

- Maintenance release.

## [1.0.4] - 2026-10-19

- The `User-Agent` header reports the installed client version. Older versions always sent `ScrapelyClient/0.0.0`.

## [1.0.3] - 2026-10-15

- The package ships the Apache-2.0 licence text and NOTICE.

## [1.0.2] - 2026-10-13

- Builds are owner-only: `build_id` on runs and metamorphs and `build` in run options are optional, since runs of someone else's Actor carry no build info. Older versions raise a validation error on those runs.
- `actor().update(default_non_owner_build=...)` sets the User Build (the build everyone else runs); `''` clears it.

## [1.0.0] - 2026-09-08

Initial release.

- Python client for the Scrapely API: Actors, runs, datasets, key-value stores, request queues, task management, and webhooks
