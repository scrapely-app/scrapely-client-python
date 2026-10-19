# Changelog

All notable changes to this project will be documented in this file.

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
