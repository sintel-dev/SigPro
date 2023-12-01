<p align="left">
<img width=15% src="https://dai.lids.mit.edu/wp-content/uploads/2018/06/Logo_DAI_highres.png" alt="DAI-Lab" />
<i>An open source project from Data to AI Lab at MIT.</i>
</p>

[![Development Status](https://img.shields.io/badge/Development%20Status-2%20--%20Pre--Alpha-yellow)](https://pypi.org/search/?c=Development+Status+%3A%3A+2+-+Pre-Alpha)
[![PyPi Shield](https://img.shields.io/pypi/v/SigPro.svg)](https://pypi.python.org/pypi/SigPro)
[![Tests](https://github.com/sintel-dev/SigPro/workflows/Run%20Tests/badge.svg)](https://github.com/sintel-dev/SigPro/actions?query=workflow%3A%22Run+Tests%22+branch%3Amaster)
[![Downloads](https://pepy.tech/badge/sigpro)](https://pepy.tech/project/sigpro)


# SigPro: Signal Processing Tools for Machine Learning

* License: [MIT](https://github.com/sintel-dev/SigPro/blob/master/LICENSE)
* Development Status: [Pre-Alpha](https://pypi.org/search/?c=Development+Status+%3A%3A+2+-+Pre-Alpha)
* Homepage: https://github.com/sintel-dev/SigPro

## Overview

SigPro offers an end-to-end solution to efficiently apply multiple *signal processing techniques*
to convert *raw time series* into *feature time series* that encode the knowledge of domain experts
in order to solve time series machine learning problems.

# Install

## Requirements

**SigPro** has been developed and tested on [Python 3.8, 3.9, 3.10, and 3.11](https://www.python.org/downloads/)
on GNU/Linux and macOS systems.

Also, although it is not strictly required, the usage of a [virtualenv](
https://virtualenv.pypa.io/en/latest/) is highly recommended in order to avoid
interfering with other software installed in the system where **SigPro** is run.

## Install with pip

The easiest and recommended way to install **SigPro** is using [pip](
https://pip.pypa.io/en/stable/):

```bash
pip install sigpro
```

This will pull and install the latest stable release from [PyPi](https://pypi.org/).

If you want to install from source or contribute to the project please read the
[Contributing Guide](CONTRIBUTING.md).


# User Guides

`SigPro` comes with the following user guides:

* [PRIMITIVES.md](PRIMITIVES.md): Information about the primitive families, their expected input
  and output.
* [USAGE.md](USAGE.md): Instructions about how to usee the three main functionalities of `SigPro`.
* [DEVELOPMENT.md](DEVELOPMENT.md): Step by step guide about how to write a valid `SigPro`
  primitive and contribute it to either `SigPro` or your own library.
