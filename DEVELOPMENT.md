
# Writing SigPro Primitives

In this document you will find a step by step guide about how to
write a valid SigPro primitive and contribute it to either SigPro or your
own library.

## 0. Set up your library

If you intend to create a `SigPro` primitive for your own library you
will need to make sure to have configured your library to allow
MLBlocks to find your primitives. In order to do so, please follow
[these steps](https://hdi-project.github.io/MLBlocks/advanced_usage/adding_primitives.html#developing-a-primitives-library).

Otherwise, if you intend to contribute your primitive to the `SigPro`
library you do not need to configure anything and you can skip this step
and proceed to writing your primitive.

## 1. Write your Python function

### Types and subtypes of functions

Once you have installed the repository, you can proceed with the creation of
a transformation or aggregation function.

First of all, you need to identify the type of function that you are going
to implement.

In `SigPro`, there are two types of functions:

* `transformations`: They are functions that take time series segments
  as transform them into a different representation format that makes
  the extraction of features easier.
* `aggregations`: They are functions that take the transformation outputs
  as input and generate one or more float values that will be used as
  features to solve Machine Learning problems.

The transformations and aggregations are further divided in three
subtypes of functions:

* Amplitude:
    * Transformations: The Amplitude Transformations take as input a
      vector of amplitude values and transform them into a new vector of
      amplitude values.
    * Aggregations: The Amplitude Aggregations take as input the amplitude
      values returned by the Amplitude Transformations and compute one
      or more float values out of them.
* Frequency:
    * Transformations: The Frequency Transformations take as input a
      vector of amplitude values and a single float value that indicates the
      sampling frequency associated with the amplitude values. The output
      of these functions are two vectors, one indicating amplitude values
      and the other one indicating the associated frequency values.
    * Aggregations: The Frequency Aggregations take as input the two vectors
      returned by the Frequency Transformations anaggregate them into one
      or more float values.
* Frequency Time:
    * Transformations: The Frequency Time Transformations take the same
      input as the Frequency Transformations, but instead of returning
      only two vectors indicating amplitude values and frequency values,
      they return a 2d matrix of amplitude values and 2 vectors, one
      indicating the frequency values, and the other one indicating the
      time values. Alternatively, the Frequency Time Transformations can
      return a single DataFrame that contains all the values.
    * Aggregations: The Frequency Time Aggregations take as input the
      output from the Frequency Time Transformations and generate one or
      more float values out of them.

### Module Path

When implementing your function, you will need to write the code in a
python module (a file called `<your-module>.py`) that needs to be placed
in the right place for the type and subtype of function that you are
implementing.

The paths where your python modules will need to be placed are:

* Transformations:
    * Amplitude: `sigpro/transformations/amplitude/<your-module>.py`
    * Frequency: `sigpro/transformations/frequency/<your-module>.py`
    * FrequencyTime: `sigpro/transformations/frequency_time/<your-module>.py`
* Aggregations:
    * Amplitude: `sigpro/aggregations/amplitude/<your-module>.py`
    * Frequency: `sigpro/aggregations/frequency/<your-module>.py`
    * FrequencyTime: `sigpro/aggregations/frequency_time/<your-module>.py`

### Module Name

When writing a python module for your function, we recommend you to create
one file for each primitive.

For example, if you are implementing an amplitude aggregation function
called `my_custom_aggregation`, we recommend you to implement the
corresponding function in the file
`sigpro/aggregations/amplitude/my_custom_aggregation.py`.

However, there will be cases where multiple functions are closely related
to each other, because they are very similar or use some common code,
and you may want to group them together as a family of primitives.
In these cases, it's acceptable to put all of them inside the same python
module.

### Implementation Examples

In the following sections we will show you an example of how to implement
a transformation and an aggregation function.

#### Transformation Example

In this example, we will show you the steps to implement a `Frequency
Transformation` that simply applies and `fft` transformation using `numpy`
and then returns the `real` part of the returned vector and the `frequency`
values returned by the `fftfreq` function, also from `numpy`.

We will call this function `fft_real`, and we will implement it in
a module called `fft.py`.

Based on the previous sections we can conclude the following properties:

* Primitive type: `transformation`
* Primitive subtype: `frequency`
* Primitive Folder: `sigpro/transformations/frequency/`
* Module Name: `fft.py`
* Function Name: `fft`
* Inputs:
    * `amplitude_values`
    * `sampling_frequency`
* Outputs:
    * `amplitude_values`
    * `frequency_values`

Based on these properties, you can create the file
`sigpro/transformations/frequency/fft.py` inside the folder
in which you have cloned our SigPro repository.

```python
import numpy as np

from cms_ml.utils import frequency_converter

def fft_real(amplitude_values, sampling_frequency):
    """Apply an FFT on the amplitude values and return the real components.

    This computes the discrete Fourier Transform using the `fft` function
    from `numpy.fft` module and then extracting the real part of the
    returned vector to discard the complex components that represent
    the phase values.
    Also compute the frequency values using the `fftfreq` from the
    same module.

    Args:
        amplitude_values (np.ndarray):
            A numpy array with the signal values.
        sampling_frequency (int, float or str):
            Sampling frequency value used for the signals.

    Returns:
        tuple:
            * `amplitude_values (numpy.ndarray)`
            * `frequency_values (numpy.ndarray)`
    """
    frequency = frequency_converter(frequency)
    amplitude_values = np.real(np.fft.fft(amplitude_values))
    frequency_values = np.fft.fftfreq(len(amplitude_values), frequency)

    return amplitude_values, frequency_values
```

### Aggregation Example

In this example, we will show you the steps to implement a `Frequency
Aggregation` that computes the mean the given amplitude values within
a specified frequency band.

We will call this function `band_mean`, and we will implement it in
a module called `band.py`.

In this case, the function will have two fixed hyperparameters,
`min_frequency` and `max_frequency`, with specify the lower and higher
ends of the frequency band.

Based on the previous sections we can conclude the following properties:

* Primitive type: `aggregation`
* Primitive subtype: `frequency`
* Primitive Folder: `sigpro/aggregation/frequency/`
* Module Name: `band.py`
* Function Name: `band_mean`
* Inputs:
    * `amplitude_values`
    * `frequency_values`
    * `min_frequency`
    * `max_frequency`
* Outputs:
    * `mean_band_value`

Based on these properties, you can create the file
`sigpro/aggregation/frequency/band.py` inside the folder
in which you have cloned our SigPro repository.


```python
import numpy as np

from sigpro.utils import frequency_converter

def band_mean(amplitude_values, frequency_values,
              min_frequency, max_frequency):
    """Compute the mean values for a specific band.

    Filter between a high and low band and compute
    the mean value for this specific band.

    Args:
        amplitude_values (np.ndarray):
            A numpy array with the signal values.
        frequency_values (np.ndarray):
            A numpy array with the frequency values.
        min_frequency (int or float):
            Band minimum.
        max_frequency (int or float):
            Band maximum.
    Returns:
        float:
            Mean value for the given band.
    """
    lower_frequency_than = frequency_values <= max_frequency
    higher_frequency_than = frequency_values >= min_frequency
    selected_idx = np.where(higher_frequency_than & lower_frequency_than)
    selected_values = amplitude_values[selected_idx]
    return np.mean(selected_values)
```

**Note:** Make sure to properly document the purpose of your function and
the inputs and outputs as shown in the example.
Also **if there is an external library used your modules, make sure that
it's specified in `setup.py` inside the list of external dependencies:
`install_requires`**.

## 2. Test your function with demo data

Once you have finished implementing your function you will want to test
it by directly passing input data to it.

`SigPro` includes functions to load demo data in the exact format that
each one of the different types of functions will expect:

* `get_amplitude_demo`: Returns amplitude values and sampling frequency used.
* `get_frequency_demo`: Returns amplitude values transformed using an `fft`
  and their corresponding frequency values.
* `get_frequency_time_demo`: Returns amplitude values, frequency values and
  time values computed using an `stft` transformation. Optionally, the output
  format can be changed to return a `pandas.DataFrame`.

These functions can be found inside the module `demo` of `sigpro` and can be
imported and used like this:

```python
from sigpro.demo import get_amplitude_demo
from sigpro.demo import get_frequency_demo
from sigpro.demo import get_frequency_time_demo
from sigpro.demo import get_demo_data 

amplitude_values, sampling_frequency = get_amplitude_demo()
amplitude_values, frequency_values = get_frequency_demo()
amplitude_values, frequency_values, time_values = get_frequency_time_demo()
dataframe = get_demo_data()
```

In all cases, the functions will return values that correspond to a
random index from the Timeseries demo returned by the `sigpro.demo.get_demo`
function. If you want to obtain a fixed index value, you can pass the
index number with the `index` argument, like this:

```python
amplitude_values, sampling_frequency = get_amplitude_demo(index=100)
```

### Testing the `fft_real` transformation

In order to test the `fft_real`, first you will import the demo data and
the function in a jupyter notebook or ipython console. In this case call the
`get_amplitude_demo` and pass its outputs to the `fft_real` function:

```python
from sigpro.demo import get_amplitude_demo
from sigpro.transformations.fft import fft_real

amplitude_values, sampling_frequency = get_amplitude_demo()

output_amplitudes, output_frequencies = fft_real(
    amplitude_values,
    sampling_frequency
)
```

### Testing the `band_mean` aggregation

In order to test the `band_mean`, first you will import the demo data and the
function in a jupyter notebook or ipython console. In this case call the
`get_frequency_demo` and pass its outputs to the `band_mean` function:

```python
from sigpro.aggregations.band import band_mean
from sigpro.demo import get_frequency_demo

amplitude_values, frequency_values = get_frequency_demo()
mean_value = band_mean(
    amplitude_values,
    frequency_values,
    min_frequency=100,
    max_frequency=200
)
```

## 3. Use `make_primitive` to create a primitive

Once you have ensured that your functions work as expected, you can
convert it into a primitive by using the `make_primitive` function from the
`contributing` module.

In order to use this function you will need to pass the name of the
primitive, which is the name of the primitive is the complete python path
of the function including the full name of the module.

For example, the names for the two functions that we created above would be:

* `sigpro.transformations.frequency.fft.fft_real`
* `sigpro.aggregations.frequency.band.band_mean`

Additionally, you will need to specify any additional arguments that
the function will need to extract from the context and the fixed and
tunable hyperparameters that the function has.

Once this information is given, this function will:

* Identify the type and subtype of your primitive based on its name.
* Validate that the inputs that the primitive expects are correct for
  its type and subtype
* Validate that the function also expects the specified context arguments
  and hyperparameters
* Validate that there are no additional arguments that have not been
  specified
* If everything is correct, create a JSON file for your primitive in the
  `primitives` folder of the repository.

You can find the complete specification of usage for this function on the
[Usage](USAGE.md) documentation.

### Making the `fft_real` primitive

In order to create the `fft_real` primitive using the `make_primitive`
function, you will have to import this function and call it with the
name of the primitive, which in this case is the complete python path to
this function: `sigpro.transformations.frequency.fft.fft_real`

As there are no extra context arguments or tunable hyperparameters, the
creation of this function is very simple and no additional information needs
to be passed:

```python
from sigpro.contributing import make_primitive

make_primitive(
    'sigpro.transformations.frequency.fft.fft_real',
    primitive_type='transformation',
    primitive_subtype='frequency'
)
```

After this, a message will be printed if the primitive JSON was successfully
created in the expected path, which in this case will be
`sigpro.transformations.frequency.fft.fft_real.json`.

If you open the file, you should see the following structure in it:

```json
{
    "name": "sigpro.transformations.frequency.fft.fft_real",
    "primitive": "sigpro.transformations.frequency.fft.fft_real",
    "produce": {
        "args": [
            {
                "name": "amplitude_values",
                "type": "numpy.ndarray"
            },
            {
                "name": "sampling_frequency",
                "type": "float"
            },
        ],
        "output": [
            {
                "name": "amplitude_values",
                "type": "numpy.ndarray"
            },
            {
                "name": "frequencies",
                "type": "numpy.ndarray"
            },
        ],
    },
    "hyperparameters": {
        "fixed": {},
        "tunable": {}
        },
    }
}
```

### Making the `band_mean` aggregation primitive

Since the `band_mean` function has a couple of fixed hyperparameters,
in order to create its JSON primitive using the `make_primitive` function
you will need to pass the fixed hyperparameters specification as follows:

```python
from sigpro.contributing import make_primitive

make_primitive(
    'sigpro.aggragations.frequency.band.band_mean',
    fixed_hyperparameters={
        'min_frequency': {
            'type': 'float',
        },
        'max_frequency': {
            'type': 'float',
        }
    }
)
```

And the JSON
`sigpro/primitives/sigpro.transformations.frequency.band.band_mean.json`
file will be generated as follows:

```json
{
    "name": "sigpro.transformations.frequency.band.band_mean",
    "primitive": "sigpro.transformations.frequency.band.band_mean",
    "produce": {
        "args": [
            {
                "name": "amplitude_values",
                "type": "numpy.ndarray"
            },
            {
                "name": "frequency_values",
                "type": "float"
            },
        ],
        "output": [
            {
                "name": "value",
                "type": "float"
            },
        ],
    },
    "hyperparameters": {
        "fixed": {
            "min_frequency": {
                "type": "float",
            },
            "max_frequency": {
                "type": "float",
            }
        },
        "tunable": {
        },
    }
}
```

## 4. Test your primitive

TODO: Explain how to set up the environment to let MLBlocks find
the primitives.

Once you have created your primitive using `make_primitive`, there is one
more step required to ensure that this primitive was correctly created,
which is to test our primitive.

To do so, we have implemented the `run_primitive` function that will use your
primitive against the demo data so you can validate that the primitive
specification is correct.

This function is available in the module `contributing` and can be imported
as follows:

```python
from sigpro.contributing import run_primitive
```

The function `run_primitive` has the following arguments:

* `primitive (str)`: Complete name of the primitive or path to the primitive.
* `tunable_hyperparameter`: Tunable hyperparameter with it's value.
* `fixed_hyperparameter`: Fixed hyperparameter and it's value.

And it does the following steps:

1. It loads the demo data as timeseries segments
2. If the primitive is a frequency or frequency_time aggregation, it
   applies an `fft` or `stft` transformation on the demo data.
3. It calls your primitive for each row in the data, passing the given
   hyperparameter values
4. Returns a list of tuples with the outputs that your primitive generated.

### Running the `fft_real` primitive

Considering the previously generated primitive,
`sigpro.transformations.frequency.fft.fft_real`, first you have to import
the `run_primitive` function and call it with the name of the primitive:

```python
from sigpro.contributing import run_primitive

output = run_primitive(
    'sigpro.transformations.frequency.fft.fft_real'
)
```

The returned `output` will be a `list` with the output that your primitive
generated for each row in the demo dataset.

### Band Mean Example

Considering the previously generated primitive,
`sigpro.transformations.frequency.band.band_mean`, first you have to import
the `run_primitive` function and call it with the name of the primitive:

```python
from sigpro.contributing import run_primitive

output = run_primitive(
    'sigpro.aggregations.frequency.band.band_mean'
    min_frequency=1000,
    max_frequency=10000
)
```
