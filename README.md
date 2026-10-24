<!-- Derived from apify-client-python (README.md), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH. -->

<h1 align="center">Scrapely API client for Python</h1>

<p align="center">
  <strong>The official Python client for the <a href="https://api.scrape.ly">Scrapely REST API</a>.</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/scrapely-client-python/"><img src="https://badge.fury.io/py/scrapely-client-python.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/scrapely-client-python/"><img src="https://img.shields.io/pypi/dm/scrapely-client-python" alt="PyPI downloads"></a>
  <a href="https://pypi.org/project/scrapely-client-python/"><img src="https://img.shields.io/badge/python-3.11%2B-blue" alt="Python versions"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/pypi/l/scrapely-client-python" alt="License"></a>
</p>

`scrapely-client-python` lets you talk to the [Scrapely platform](https://api.scrape.ly) from Python — run Actors, manage storages (datasets, key-value stores, request queues), schedule tasks, configure webhooks, and use everything else exposed by the Scrapely API. It ships both synchronous and asynchronous clients, fully typed responses, automatic retries with exponential backoff, tiered timeouts, pagination helpers, streaming, and a pluggable HTTP layer.

> If you want to **build** Actors in Python rather than consume the API, use the Scrapely SDK for Python instead — it bundles this client and adds Actor-side primitives.

## Table of contents

- [Installation](#installation)
- [Quick start](#quick-start)
- [Features](#features)
- [Usage examples](#usage-examples)
- [Documentation](#documentation)
- [Related projects](#related-projects)
- [Support and community](#support-and-community)
- [Contributing](#contributing)
- [License](#license)

## Installation

`scrapely-client-python` requires **Python 3.11 or higher** and is published on [PyPI](https://pypi.org/project/scrapely-client-python/).

- From [PyPI](https://pypi.org/project/scrapely-client-python/), it can be installed for example with [pip](https://pip.pypa.io/):

    ```bash
    pip install scrapely-client-python
    ```

    or with [uv](https://docs.astral.sh/uv/):

    ```bash
    uv add scrapely-client-python
    ```

    or any other Python package manager that consumes PyPI.

    The client compresses request bodies with `gzip` by default (no extra dependencies required). To opt in to
    `brotli` (better compression ratio), install the optional extra and pass `compression='brotli'`:

    ```bash
    pip install "scrapely-client-python[brotli]"
    # or
    uv add "scrapely-client-python[brotli]"
    ```


## Quick start

You'll need a Scrapely API token — find yours in the integrations section of the Scrapely dashboard. Pass it to the client and you're ready to go.

The client sends requests to `https://api.scrape.ly` unless you pass another API origin as `api_url`. When `api_url` is not given, the `SCRAPELY_API_URL` environment variable sets it (for example `SCRAPELY_API_URL=https://api-staging.scrape.ly`). `api_public_url`, used for public storage links, keeps its own argument and default. The client does not read the token from the environment.

### Synchronous client

```python
from scrapely_client import ScrapelyClient

client = ScrapelyClient('MY-SCRAPELY-TOKEN')

# Start an Actor and wait for it to finish.
run = client.actor('my-user/hello-world').call(
    run_input={'message': 'Hello, Scrapely!'},
)
if run is None:
    raise RuntimeError('Actor run was not found.')

# Iterate items from the run's default dataset.
for item in client.dataset(run.default_dataset_id).iterate_items():
    print(item)
```

### Asynchronous client

```python
import asyncio

from scrapely_client import ScrapelyClientAsync


async def main() -> None:
    client = ScrapelyClientAsync('MY-SCRAPELY-TOKEN')

    run = await client.actor('my-user/hello-world').call(
        run_input={'message': 'Hello, Scrapely!'},
    )
    if run is None:
        raise RuntimeError('Actor run was not found.')

    # Iterate items from the run's default dataset.
    async for item in client.dataset(run.default_dataset_id).iterate_items():
        print(item)


asyncio.run(main())
```

> **Keep your token secret.** It authorizes requests on your behalf and can incur usage costs. Never commit it to source control or expose it to client-side code.

## Features

- **Synchronous and asynchronous clients** — pick `ScrapelyClient` or `ScrapelyClientAsync` to match your codebase; both expose the same API (Asyncio support).
- **Fully typed responses** — every method returns a [Pydantic](https://docs.pydantic.dev/) model generated from the platform's OpenAPI spec, with IDE autocomplete and runtime validation (Typed models).
- **Automatic retries** — exponential backoff for network errors, HTTP 429, and 5xx responses, configurable per client (Retries).
- **Tiered timeouts** — short / medium / long tiers picked per endpoint, overridable per call (Timeouts).
- **Pagination and streaming** — iterate datasets, key-value store keys, or live logs without manual paging or buffering (Pagination, Streaming).
- **Convenience methods** — `call()`, `wait_for_finish()`, nested resource access, and other shortcuts that hide platform quirks (Convenience methods).
- **Pluggable HTTP layer** — swap the default Impit-based HTTP client for `httpx`, `requests`, `aiohttp`, or any custom implementation (Custom HTTP clients).
- **Structured errors** — every API error surfaces as a `ScrapelyApiError` with HTTP-specific subclasses for precise handling (Error handling).
- **Debug logging** — opt-in structured logging on the `scrapely_client` logger captures request URLs, status codes, retry attempts, and more (Logging).

## Usage examples

The client mirrors the platform's resource model. Each entry point returns either a **single-resource client** for an individual item or a **collection client** for listing and creating items (Single and collection clients).

### List Actors and create one

```python
actors = client.actors()
print(actors.list(limit=10).items)

new_actor = actors.create(name='my-actor')
```

### Stream live logs while a run is in progress

```python
run = client.actor('my-user/web-scraper').start(run_input={...})

with client.run(run.id).log().stream() as log_stream:
    for chunk in log_stream.iter_bytes():
        print(chunk.decode(), end='')
```

### Read and write key-value store records

```python
store = client.key_value_store('STORE-ID')
store.set_record('greeting', {'message': 'Hello!'})
record = store.get_record('greeting')
```

### Iterate dataset items with automatic pagination

```python
for item in client.dataset('DATASET-ID').iterate_items(fields=['title', 'url']):
    process(item)
```

### Create and run an automation

```python
automation = client.automations().create({
    'title': 'Daily dentists',
    'trigger': {'kind': 'schedule', 'cron': '0 9 * * *', 'timezone': 'Europe/Berlin'},
    'steps': [{'kind': 'savedInput', 'savedInputId': 'SAVED-INPUT-ID'}],
    'ai': {'mode': 'summarize', 'prompt': 'List the new practices with their phone numbers.'},
    'deliveries': [{'channel': 'email'}],
})
run = client.automation(automation['id']).run()
```

Automations take and return the API's camelCase dictionaries (see the automations section of the API reference).

### Tune retries and timeouts

```python
from datetime import timedelta

from scrapely_client import ScrapelyClient

client = ScrapelyClient(
    token='MY-SCRAPELY-TOKEN',
    max_retries=8,
    min_delay_between_retries=timedelta(milliseconds=500),
    timeout_long=timedelta(minutes=10),
)
```

For end-to-end recipes — passing input, managing tasks for reusable input, retrieving and merging Actor data, integrating with Pandas, plugging in a custom HTTP client — see the Guides.

## Documentation

The full documentation lives at **https://api.scrape.ly**.

| Section | What you'll find |
| --- | --- |
| Introduction | Overview, prerequisites, and a tour of the client. |
| Quick start | Authenticate, run an Actor, and fetch its results step by step. |
| Concepts | Asyncio, single vs. collection clients, nested clients, error handling, retries, logging, convenience methods, pagination, streaming, custom HTTP clients, timeouts. |
| Guides | Pass input to an Actor, manage tasks for reusable input, retrieve Actor data, integrate with data libraries (e.g. Pandas), use HTTPX as the HTTP client. |
| API reference | Generated reference for every class, method, and model. |
| Changelog | Release history and breaking changes. |

## Related projects

- **Scrapely SDK for Python** — toolkit for **building** Actors in Python (this client is bundled with it).
- **[Crawlee for Python](https://crawlee.dev/python)** — high-level web scraping and browser automation framework that powers many Actors.
- **Scrapely API client for JavaScript / TypeScript** — equivalent Scrapely API client for Node.js.
- **Scrapely SDK for JavaScript / TypeScript** — equivalent Scrapely SDK for Node.js.
- **[Crawlee for JavaScript / TypeScript](https://crawlee.dev)** — the Node.js implementation of the Crawlee framework.
- **Scrapely CLI** — command-line tool for interacting with the Scrapely platform: managing Actors, runs, storages, local development, and deployment.

## Support and community

- **GitHub issues** — report a bug or request a feature in the repository's issue tracker.

## Contributing

Bug reports, fixes, and improvements are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for the development setup, coding standards, testing, and the release process. The repo uses [uv](https://docs.astral.sh/uv/) for project management and [Poe the Poet](https://poethepoet.natn.io/) as a task runner; the typical loop is:

```bash
uv run poe install-dev   # install dev deps and git hooks
uv run poe check-code    # lint, type-check, unit tests, docstring check
```

## License

Released under the [Apache License 2.0](./LICENSE); see [NOTICE](./NOTICE).
