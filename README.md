# Signhost Api Python Client

[![PyPI](https://img.shields.io/pypi/v/signhost-api-python-client.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/signhost-api-python-client.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/signhost-api-python-client)][python version]
[![License](https://img.shields.io/pypi/l/signhost-api-python-client)][license]

[![Read the documentation at https://signhost-api-python-client.readthedocs.io/](https://img.shields.io/readthedocs/signhost-api-python-client/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/foarsitter/signhost-api-python-client/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/foarsitter/signhost-api-python-client/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/signhost-api-python-client/
[status]: https://pypi.org/project/signhost-api-python-client/
[python version]: https://pypi.org/project/signhost-api-python-client
[read the docs]: https://signhost-api-python-client.readthedocs.io/
[tests]: https://github.com/foarsitter/signhost-api-python-client/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/foarsitter/signhost-api-python-client
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

- 100% test coverage

## Requirements

- httpx
- pydantic
- attrs
- click

## Installation

You can install _Signhost Api Python Client_ via [pip] from [PyPI]:

```console
$ pip install signhost-api-python-client
```

## Usage

```python
import io
from signhost import models
from signhost.client import DefaultClient

signhost = DefaultClient(api_key="str", app_key="str")
transaction = models.Transaction(signers=[models.Signer(email="str")])

transaction = signhost.transaction_init(transaction=transaction)
signhost.transaction_file_put(
    transaction.Id,
    "file.pdf",
    io.BytesIO(b"test"),
)
transaction = signhost.transaction_start(transaction.Id)

print("Sign the contract over here", transaction.Signers[0].SignUrl)

signhost.transaction_get(transaction.Id)
signhost.transaction_file_get(transaction.Id, "file.pdf")
signhost.receipt_get(transaction.Id)
```

### Async support

```python
from signhost.client import AsyncClient

async with AsyncClient(api_key="str", app_key="str") as signhost:
    signhost.transaction_get("xyz")
```

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Signhost Api Python Client_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was initiated by [dok.legal] and was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[dok.legal]: https://dok.legal/
[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/foarsitter/signhost-api-python-client/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/foarsitter/signhost-api-python-client/blob/main/LICENSE
[contributor guide]: https://github.com/foarsitter/signhost-api-python-client/blob/main/CONTRIBUTING.md
[command-line reference]: https://signhost-api-python-client.readthedocs.io/en/latest/usage.html
