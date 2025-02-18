# History

## 0.3.0 - 2025-02-17

### Features
* Add Support for Python 3.12 & Remove 3.8 - [Issue #63](https://github.com/sintel-dev/SigPro/pull/63) by @sarahmish
* Add fft frequency transformation - [Issue #62](https://github.com/sintel-dev/SigPro/pull/62) by @SaraPido
* Band rms - [Issue #61](https://github.com/sintel-dev/SigPro/pull/61) by @SaraPido


## 0.2.1 - 2024-04-24

### Features

* Frequency primitive - [Issue #60](https://github.com/sintel-dev/SigPro/pull/60) by @SaraPido 


## 0.2.0 - 2024-02-02

### Features
* Demo Notebooks for Pipeline usage  - [Issue #55](https://github.com/sintel-dev/SigPro/issues/55) by @andyx13
* Added `contributing_primitive` and `basic_primitives` module to assist with new primitive creation/usage   - [Issue #54](https://github.com/sintel-dev/SigPro/issues/54) by @andyx13
* Incorrect classification for stft.json and stft_real.json - [Issue #53](https://github.com/sintel-dev/SigPro/issues/53) by @andyx13
* Support for more complex pipeline architectures - [Issue #52](https://github.com/sintel-dev/SigPro/issues/52) by @andyx13
* Update primitive interfaces - [Issue #51](https://github.com/sintel-dev/SigPro/issues/51) by @andyx13
* Syntax for pipeline creation - [Issue #41](https://github.com/sintel-dev/SigPro/issues/41) by @andyx13
* Load demo dataset at random index - [Issue #35](https://github.com/sintel-dev/SigPro/issues/35) by @andyx13


## 0.1.2 - 2023-12-11

### Features
* Python version update - [Issue #44](https://github.com/sintel-dev/SigPro/issues/44) by @andyx13
* Add demo notebook and per-primitive documentation - [Issue #47](https://github.com/sintel-dev/SigPro/issues/47) by @andyx13


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
