# SigPro Primitives

In this document you will find information about what kind of primitives `SigPro` contains and
the type and subtypes of those, with a detailed information about their input and output
considering the type and subtype of the primitive.

## Overview

The goal of SigPro is to be able to process *time series* data passed as
time stamped *time series segments* and extract *feature time series* from
them by applying multiple types of *transformations* and *aggregations*.

## Transformations and Aggregations

All the timeseries processing in SigPro happens in two families of
functions:

* Transformations: They convert time series segment vectors into new
  vectors that represent the same information in a different format.
* Aggregations: They convert time series segment vectors or transformed
  representations of them into individual features.

### Transformations

Transformations are simple Python functions that transform 1d arrays of
time series values into other arrays of values of 1, 2 or 3 dimensions.
These transforms can be in time domain or frequency domain and/or joint
time frequency domain.

#### Input

The input format for the transformation functions is always at least a 1d
numpy array. Optionally, functions can accept additional variables as
input, such as the sampling frequency, contextual values or
hyperparameters.

#### Types of transformations

##### Amplitude transformations

These transformations take as input a 1d array of values and return another
1d array of values. The returned array does not necessarily have the same
length as the inputted one.

* Input:
    * `amplitude_values`: 1d array of values.
    * `**context_values`: additional variables from the context.
    * `**hyperparameters`: additional arguments to control the behavior.
* Output
    * `transformed`: 1d array of values.

```python
def amplitude_transform(
        amplitude_values: np.ndarray,
        **context_values,
        **hyperparameter_values,
    ) -> np.ndarray:
```

###### Examples

The simplest example of this type of transformation is the `identity`,
which receives a time series segment as input and returns it unmodified:

```python
def identity_transform(amplitude_values):
    return amplitude_values
```

A more complex example which would use contextual information as well as
hyperparameters would look like this:


```python
def complex_transform(amplitude_values, a_context_value, a_hyperparam):
    # here we would manipulate the values based on `a_context_value`
    # and a_hyperparam value.
    ...
    return transformed_values
```

##### Frequency transformations

These transformations take as input a 1d array of time series values and a
sampling frequency, and perform a frequency based transformations.

The outputs are 2 1d arrays, the first one being the frequency amplitudes
and the other one being the associated frequencies.

* Input:
    * `amplitude_values`: 1d array of values.
    * `sampling_frequency`: sampling frequency.
    * `**context_values`: additional variables from the context.
    * `**hyperparameters`: additional arguments to control the behavior.
* Output
    * `transformed`: 1d array of values.
    * `frequencies`: 1d array of frequency values.

```python
def spectrum_analysis_transform(
        amplitude_values: np.ndarray,
        sampling_frequency: float,
        **context_values,
        **hyperparameter_values,
    ) -> tuple[np.ndarray]:
```

###### Examples

An example of this is the `fft`, which receives a time segment and a
sampling frequency as input and returns the fft amplitudes and frequencies
as output.

```python
import numpy as np

def fft_transform(amplitude_values, sampling_frequency):
    amplitude_values = np.fft.fft(amplitude_values)
    frequency_values = np.fft.fftfreq(len(amplitude_values), sampling_frequency)
    return amplitude_values, frequency_values
```

##### Frequency Time (2D Spectrum analysis) transformations

These transformations take as input a 1d array of values and a sampling
frequency, and perform multiple frequency based transformations over
multiple points in time within the sequence.

The outputs are TBD

* Input:
    * `values`: 1d array of values.
    * `sampling_frequency`: sampling frequency.
    * `**context_values`: additional variables from the context.
    * `**hyperparameters`: additional arguments to control the behavior.
* Output
    * `dataframe`

```python
def spectrum_2d_analysis_transform(
        amplitude_values: np.ndarray,
        sampling_frequency: float,
        **context_values,
        **hyperparameter_values,
    ) -> (np.ndarray, np.ndarray, np.ndarray)
```

An example of this is the `stft`, which receives a time segment and a
sampling frequency as input and returns a vector with multiple fft
transformations applied in different points in time over the input segment:

```python
import scipy.signal

def stft(amplitude_values, sampling_frequency):
    frequency_values, time_values, amplitude_values = scipy.signal.stft(
        amplitude_values,
        fs=sampling_frequency
    )
    return amplitude_values, frequency_values, time_values
```

### Aggregations

Transforms simply convert the signal into an alternate representation. They
don't directly result in `features` for machine learning or even a
feature time series. In general, further aggregations need to be applied to
the output from the transforms. In general these aggregations are of three
kinds:

* `Statistical aggregations`: This just aggregate using different
  statistical functions - rms value, mean value, and several others.
* `Spectral aggregations`: These are very domain specific and this is where
  an expert can put their intelligence. These could be something like total
  energy in the frequency bin 10-100Mhz. As a result, the input to these
  aggregations is both the ```amplitude_values``` output, but also the
  ```frequencies```. And similarly, if the transform is joint time-frequency
  transform, then the data frame is provided.
* ```Comparitive aggregations```: These are special aggregations, where along
  side the information from the transformation, a reference is also provided.
  This reference can be from physics based simulation, or transform of a
  neighboring window, or data from a known problematic scenario.

#### Input

The input format for these aggregations is the output from the different
transformations + optional additional context values or hyperparameters.

The outputs are always one float value or a tuple with multiple float
values.

#### Aggregation Types

##### Amplitude aggregations

These aggregations take as input a 1d array of values.

* Input:
    * `amplitude_values`: 1d array of values.
    * `**context_values`: additional variables from the context.
    * `**hyperparameters`: additional arguments to control the behavior.
* Output
    * `feature` or `features`: single float value, or tuple with multiple
      float values.

```python
def statistical_aggregation(
        amplitude_values: np.ndarray,
        **context_values,
        **hyperparameter_values,
    ) -> float or tuple[float]:
```

An example of such an aggregation is a simple mean:

```python
import numpy as np

def mean(values):
    return np.mean(values)
```

##### Frequency aggregations (Spectrum analysis)

These transformations take as input a 2 1d arrays, one containing
amplitude values and the other one containing frequency values.

* Input:
    * `amplitude_values`: 1d array of values.
    * `frequency_values`: 1d array of frequency values.
    * `**context_values`: additional variables from the context.
    * `**hyperparameters`: additional arguments to control the behavior.
* Output
    * `feature` or `features`: single float value, or tuple with multiple
      float values.

```python
def spectrum_analysis_aggregation(
        amplitude_values: np.ndarray,
        frequency_values: np.ndarray,
        **context_values,
        **hyperparameter_values,
    ) -> float or tuple[float]:
```


##### Frequency time aggregations (2D Spectrum analysis)

These transformations take as input the output of the frequency time
transforms.

* Input:
    * `amplitude_values`: transformed amplitude values from transformation
       output.
    * `frequency_values`: frequency values from transformation output.
    * `time_values`: time values from transformation output.
    * `**context_values`: additional variables from the context.
    * `**hyperparameters`: additional arguments to control the behavior.
* Output
    * `feature` or `features`: single float value, or tuple with multiple
      float values.

```python
def spectrum_2d_analysis_aggregation(
        dataframe: pd.DataFrame,
        **context_values,
        **hyperparameter_values,
    ) -> float or tuple[float]:
```
