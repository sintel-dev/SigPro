# History

## 0.1.1 - 2023-04-06

### Features
* Accepting single value data frame format - [Issue #36](https://github.com/sintel-dev/SigPro/issues/36) by @frances-h @sarahmish
* Update demos - [Issue #26](https://github.com/sintel-dev/SigPro/pull/26) by @frances-h

## 0.1.0 - 2021-11-14

### Features
* Rework SigPro to be class based

## 0.0.3 - 2021-09-27

### Features
* Add `process_signals` function to take a collection of primitives and create features for the given data. 

## 0.0.2 - 2021-02-05

### Bug Fixes

* `MANIFEST.in`: copy the json files of the primitives with the package installation.

## 0.0.1 - 2021-01-26

First release to PyPI.

This release comes with the first version of the `contributing` module, which makes it easier
to create new primitives and to test those with the demo data included in this package.

This release also includes the following User Guides:

* [PRIMITIVES.md](https://github.com/sintel-dev/SigPro/blob/master/PRIMITIVES.md): Information
  about the primitive families, their expected input and output.
* [USAGE.md](https://github.com/sintel-dev/SigPro/blob/master/USAGE.md): Instructions about how
  to usee the three main functionalities of `SigPro`.
* [DEVELOPMENT.md](https://github.com/sintel-dev/SigPro/blob/master/DEVELOPMENT.md): Step by step
  guide about how to write a valid `SigPro` primitive and contribute it to either `SigPro` or
  your own library.

### Features

* Demo data: Available demo data to test primitives.
* First primitives: The following list of primitives were added:
  * `sigpro.aggregations.amplitude.statistical.crest_factor`
  * `sigpro.aggregations.amplitude.statistical.kurtosis`
  * `sigpro.aggregations.amplitude.statistical.mean`
  * `sigpro.aggregations.amplitude.statistical.rms`
  * `sigpro.aggregations.amplitude.statistical.skew`
  * `sigpro.aggregations.amplitude.statistical.std`
  * `sigpro.aggregations.amplitude.statistical.var`
  * `sigpro.transformations.amplitude.identity.identity`
  * `sigpro.transformations.frequency.fft.fft`
  * `sigpro.transformations.frequency.fft.fft_real`
  * `sigpro.transformations.frequency_time.stft.stft`
  * `sigpro.transformations.frequency_time.stft.stft_real`
* Contributing module.
* Documentation on how to contribute new primitives and how to run those.
