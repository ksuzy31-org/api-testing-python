<h1 align="center">Virta EV Station API Testing (Python)</h1>

<p align="center">  
This application is built to do REST API testing using python scripts along with the use of Pytest module as our testing framework.
</p>

<p align="center">
  <a href="https://opensource.org/licenses/Apache-2.0"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"/></a>
</p>

# Demo
![Page-Object-Model-Demo-Gif.gif](demo/pyrestapitest_demo.gif)


## Languages, libraries and tools used

* __[Python](https://www.python.org/downloads/)__
* __[Pytest](https://docs.pytest.org/en/6.2.x/getting-started.html)__
* __[Requests](https://docs.python-requests.org/en/master/)__
* __[JsonPath](https://pypi.org/project/jsonpath/)__
* __[Pycharm](https://www.jetbrains.com/pycharm/download/)__

Above Features are used to make code simple, generic, understandable, clean and easily maintainable for future development.

## Installation

Install the dependencies and start the testing.

 __Install Pytest__:
```sh
pip3 install --user -U pytest
```
 __Install Requests__:
```sh
pip3 install --user requests
```

 __Install Json Path__:
```sh
pip3 install --user jsonpath
```
## Automated tests

__To run a test, you can simply write the following command on Terminal__:
```sh
pytest
```

__To run and get details of all the executed test, you can simply write the following command on Terminal__:
```sh
pytest -rA
```

__To run and generate full HTML details report of all the executed test, you can simply write the following commands on Terminal__:

__But first install [Pytest-HTML](https://pypi.org/project/pytest-html/) by writing the following command on Terminal__
```sh
pip3 install --user pytest-html
```
__Then write the following command on Terminal__
```sh
pytest --html=YOUR_REPORT_FILE_NAME.html
```

__To see the reports, open the Project window, and then right-click then click on refresh then right-click on __StationReport.html__ to open the file on the default browser.__

![Page-Object-Model-Demo-Gif.gif](demo/pyrestapitest-report-file.png)

---

## Usage Example

A minimal example using the HTTP layer to fetch station data:

```python
from session import HTTPSession, RequestTypes, Endpoints

params = {"latMin": 60.164101, "latMax": 60.164104, "longMin": 24, "longMax": 25}
status_code, data = HTTPSession.send_request(RequestTypes.GET, Endpoints.STATIONS, params)
print(status_code, type(data))  # e.g., '200', <class 'list'>
```

Notes:
- The `do_logging` flag in `params` controls request logging. It defaults to `True`. Set `{"do_logging": False}` to skip logging.
- On `requests` exceptions, `send_request` returns `None`.

---

## Logging

- Logs are written to the console and appended to `tests_output.log` in the repository root.
- Tests mock logging to avoid file I/O during runs.
- There is no rotation; the file grows over time. Delete it if it becomes too large.

---

## Status Code Comparison Note

- `StatusCodes.STATUS_200` is `'200'` (a string). The custom `assert_equal` compares stringified values by default to avoid type fragility.
- For strict type comparisons, pass `compare_types=True` to `assert_equal`.

---

## Troubleshooting Test Discovery

If `pytest` has trouble collecting tests, try targeting the file or specific tests directly:

```bash
python3 -m pytest -q tests/test_stations.py
python3 -m pytest -q -k test_send_request_handles_request_exception_and_returns_none
python3 -m pytest -vv
```

---

## Contributing / Development Notes

- Prefer behavior-focused tests that mock external effects (network, file I/O).
- Patch `session.requests.get` and `session.Logger.log_request` in tests to ensure determinism and isolation.
- Keep tests small and readable; avoid mocking internal implementation details unnecessarily.
- Use the provided constants in `test_utils.py` for station schema expectations.

---

## License

This project references the **Apache-2.0** license. Ensure a `LICENSE` file is present or review the badge link for details:

- https://opensource.org/licenses/Apache-2.0

---

# Prerequisites
* __Python__
* __Any IDE__

# Built With

* __[Python](https://www.python.org/downloads/)__ - Language used to build the application.
* __[Pycharm](https://www.jetbrains.com/pycharm/download/)__ - The IDE for writing Automation Test Scripts
