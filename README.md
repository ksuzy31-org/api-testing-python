# Virta EV Station API Testing (Python)

A lightweight example project for testing a REST API endpoint returning EV station data. It demonstrates:
- A simple HTTP session wrapper for GET requests
- Custom assertions and logging
- Deterministic unit tests using mocking

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Usage Example](#usage-example)
- [Logging](#logging)
- [Reports (pytest-html)](#reports-pytest-html)
- [Troubleshooting](#troubleshooting)
- [Contributing / Development Notes](#contributing--development-notes)
- [License](#license)

---

## Overview

This repository contains a small Python test suite that validates the response and schema of an EV station API. External effects (network and file I/O) are mocked in tests to keep them deterministic and fast.

Demo assets:
- Animated test demo: `demo/pyrestapitest_demo.gif`
- Example report screenshot: `demo/pyrestapitest-report-file.png`

---

## Requirements

- Python 3.8+
- `requests`
- `pytest` (for running tests)

---

## Quick Start

```bash
# from repository root
python3 -m pip install --user requests pytest
python3 -m pytest -q
```

---

## Installation

Install dependencies locally (user scope):

```bash
python3 -m pip install --user requests
python3 -m pip install --user -U pytest
```

---

## Running Tests

Run the entire test suite:

```bash
python3 -m pytest -q
```

Run specific file or test:

```bash
python3 -m pytest -q tests/test_stations.py
python3 -m pytest -q -k test_send_request_handles_request_exception_and_returns_none
python3 -m pytest -vv
```

---

## Usage Example

Minimal example using the HTTP layer to fetch station data:

```python
from session import HTTPSession, RequestTypes, Endpoints

params = {"latMin": 60.164101, "latMax": 60.164104, "longMin": 24, "longMax": 25}
status_code, data = HTTPSession.send_request(RequestTypes.GET, Endpoints.STATIONS, params)
print(status_code, type(data))  # e.g., '200', <class 'list'>
```

Notes:
- The optional `do_logging` flag in `params` controls request logging and defaults to `True`. Use `{"do_logging": False}` to disable.
- On `requests` exceptions, `send_request` returns `None`.
- `StatusCodes.STATUS_200` is `'200'` (string). The custom `assert_equal` compares stringified values by default; pass `compare_types=True` for strict type equality.

---

## Logging

- Logs are written to the console and appended to `tests_output.log` in the repository root.
- Tests patch logging to avoid file writes.
- There is no rotation; delete the log if it becomes too large.

---

## Reports (pytest-html)

Generate an HTML report for test results:

```bash
python3 -m pip install --user pytest-html
python3 -m pytest --html=report.html -q
```

Open the generated `report.html` in your browser. A sample screenshot is available at `demo/pyrestapitest-report-file.png`.

---

## Troubleshooting

- If test discovery fails, try targeting the specific file or running with verbosity:

```bash
python3 -m pytest -q tests/test_stations.py
python3 -m pytest -vv
```

- Network calls and logging are mocked in tests. If you see unexpected file writes or network calls, ensure your tests patch `session.requests.get` and `session.Logger.log_request` correctly.

---

## Contributing / Development Notes

- Prefer behavior-focused tests that mock external effects (network, file I/O).
- Patch `session.requests.get` and `session.Logger.log_request` to ensure deterministic tests.
- Keep tests small and readable; avoid mocking internal implementation details unnecessarily.
- Use constants in `test_utils.py` to keep schema expectations consistent.

---

## License

This project is licensed under the **Apache-2.0** license. See the license badge/reference below and ensure a `LICENSE` file is present.

- https://opensource.org/licenses/Apache-2.0

---

## Demo

![Testing demo animation](demo/pyrestapitest_demo.gif)

![HTML report screenshot](demo/pyrestapitest-report-file.png)
