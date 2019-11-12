<!--suppress HtmlDeprecatedAttribute-->
<div align="center">

# AsyncIO A2S (Any to Server) Query Library

[![CI Workflow Status](https://github.com/insurgency/aioa2squery/workflows/Run%20CI%20Workflow/badge.svg)](https://github.com/insurgency/aioa2squery/actions) [![Codecov Coverage Report](https://img.shields.io/codecov/c/github/insurgency/aioa2squery?color=F01F7A&label=Codecov&logo=Codecov&logoColor=white&style=flat-square)](https://codecov.io/gh/insurgency/aioa2squery) [![PyUp Dependency Updates](https://pyup.io/repos/github/insurgency/aioa2squery/shield.svg)](https://pyup.io/repos/github/insurgency/aioa2squery/) [![Sonatype DepShield Dependency Vulnerabilities](https://depshield.sonatype.org/badges/insurgency/aioa2squery/depshield.svg)](https://depshield.github.io) [![Supported Python Versions](https://img.shields.io/github/pipenv/locked/python-version/insurgency/aioa2squery/latest?color=3776AB&label=Python&logo=Python&logoColor=white&style=flat-square)](https://github.com/insurgency/aioa2squery/blob/latest/Pipfile) [![GitHub Package Registry Downloads](https://shields-staging-pr-4101.herokuapp.com/github/packages/downloads/insurgency/aioa2squery/total/a2squery?color=2188FF&label=Docker%20Pulls&logo=Docker&logoColor=white&style=flat-square)](https://github.com/insurgency/aioa2squery/packages) [![Discord Invite](https://img.shields.io/discord/380877117237493760.svg?color=7289DA&label=Discord&logo=discord&logoColor=white&style=flat-square)](https://insurgency.gg/discord)

</div>

This lightweight library is an [AsyncIO](https://docs.python.org/3/library/asyncio) implementation of the Any to Server (A2S) [Source Engine server query protocol](https://developer.valvesoftware.com/wiki/Server_queries).

---

## Installation

```bash
$ # Install directly from GitHub with pip:
$ pip3 install -U git+https://github.com/insurgency/aioa2squery.git@latest
$ # Or using Pipenv instead of pip:
$ pipenv install git+https://github.com/insurgency/aioa2squery.git@latest#egg=aioa2squery
$ # Or just try it out in Docker...
$ docker run --rm -it docker.pkg.github.com/insurgency/aioa2squery/a2squery:latest ...
```

<div align="center">

<!--suppress HtmlRequiredAltAttribute -->
<!-- a2squery query -t .3 --info --csv 155.133.234.0/24 185.25.183.0/24 208.78.167.0/24 -->
![](https://insurgency.github.io/aioa2squery/_images/demo.svg)

</div>

## Example

It's very easy to get started in writing concurrent queries:

```python
import asyncio
from ipaddress import ip_network
from aioa2squery import A2SQueryContext

async def main():
    # Start off with a query context (query client) 
    client = A2SQueryContext()
    # Create an iterable of queries for each target host
    queries = [client.query_info(host=str(ip)) for ip in ip_network('155.133.234.0/24')]
    # Wait a few seconds for queries to complete concurrently
    completed, _ = await asyncio.wait(queries, timeout=3)

    for response in completed:
        if not response.exception():
            # Successful query responses return a 2 tuple of the data and ping in millisecond resolution
            response, ping = response.result()
            print(f"Found a {response.game} game in {ping}ms")

asyncio.run(main())
```

## Documentation

<!-- https://docs.readthedocs.io/en/latest/custom_domains.html -->
Documentation is currently available on GitHub pages [here](https://insurgency.github.io/aioa2squery/).

## Performance Benchmarks

There's no formal performance benchmarks yet, but in simple programs I'm able to get well over 3,000+ pps/queries per second. If you're looking for significantly better performance than this library is able to provide you can look at @rumblefrog's [Go implementation](https://github.com/rumblefrog/go-a2s) or the [native reference library implementation](https://developer.valvesoftware.com/wiki/Source_Server_Query_Library). Realistically though I recommend you keep client query rates well bellow your system's configured `ulimits` for better reliability.

---

#### Donate

<sub>Donations help financially support the developers who create and work on our open source projects.</sub>

<table>
    <thead>
        <tr>
            <th><img alt="PayPal" src="https://img.shields.io/badge/-PayPal-00457C?style=flat-square&logo=paypal&longCache=true"></th>
            <th><img alt="Bitcoin" src="https://img.shields.io/badge/-Bitcoin-F7931A?style=flat-square&logo=bitcoin&longCache=true"></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b><a href="https://insurgency.gg/donate">insurgency.gg/donate</a></b></td>
            <td><a rel="payment" href="bitcoin://1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"><code>1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2</code></a></td>
        </tr>
    </tbody>
</table>
