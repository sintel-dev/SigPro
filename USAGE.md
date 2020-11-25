# SigPro Usage Guide

## Find primitives

Before you start using any SigPro primitive you will to find the
ones that are suitable for your task.

This can be done with the `sigpro.get_primitives` function.

In order to get the complete list of primitives available you can
call it without any arguments:

```python=
from sigpro import get_primitives

get_primitives()
```

The output will be a list with the names of all the primitives
that SigPro is able to find:

```
['sigpro.aggregations.amplitude.statistical.crest_factor',
 'sigpro.aggregations.amplitude.statistical.kurtosis',
 'sigpro.aggregations.amplitude.statistical.mean',
 'sigpro.aggregations.amplitude.statistical.rms',
 'sigpro.aggregations.amplitude.statistical.skew',
 'sigpro.aggregations.amplitude.statistical.std',
 'sigpro.aggregations.amplitude.statistical.var',
 'sigpro.transformations.amplitude.identity.identity',
 'sigpro.transformations.frequency.fft.fft',
 'sigpro.transformations.frequency.fft.fft_real',
 'sigpro.transformations.frequency_time.stft.stft',
 'sigpro.transformations.frequency_time.stft.stft_real']
```

### Filter primitives by Type and Subtype

In most cases you will want to search for a primitive of a specific
type or subtype.

In order to do this, you can pass the `type` and `subtype` arguments
to the `get_primitives` function.

For example, if you only want to obtain the list of *frequency transformation* primitives you can
call `get_primitives` like this:

```python=
get_primitives(type='transformation', subtype='frequency')
```

### Filter primitives by Name

If you want to narrow the search bases on the name of the primitives
you can pass a *string pattern*, and `get_primitives` will return only
the primitives that match the indicated pattern.

For example, if we are interested only in *frequency transformation*
primitives based on *fft* we can call `get_primitives` as follows:

```python=
get_primitives('fft', type='transformation', subtype='frequency')
```

## Run a Primitive

SigPro primitives can be run in a standalone mode, which allows exploring
their behavior for learning or debugging purposes.

In order to do this you can use the `run_primitive` function passing
the name of the primitive that you want to run.

For example, if you want to run the
`sigpro.aggregations.amplitude.statistical.mean` primitive you can use:

```python=
from sigpro import run_primitive

run_primitive('sigpro.aggregations.amplitude.statistical.mean')
```

This will do the following steps:

* Load the indicate primitive.
* Load demo data of the corresponding type and subtype. In this case, this
  will load the Amplitude Aggregation demo data using the
 `get_amplitude_demo`.
* Call the indicated primitive passing a randomly selected row from the
  loaded demo data.
* Return the primitive output value (or values).

### Selecting the data which the primitive runs on

In some cases you will want to run the primitive multiple times on the
same values instead of randomly selecting one row from the demo data.

In order to restrict the execution to particular demo row, you can
pass the `demo_row_index` value indicating the row that you want to use.

```python=
run_primitive(
    'sigpro.aggregations.amplitude.statistical.mean',
    demo_row_index=1
)
```

In this case, the row used by the `run_primitive` function will be the
one returned by the `get_amplitude_demo` when passing the same row index
as input:

```python=
from sigpro.demo import get_amplitude_demo

row = get_amplitude_demo(index=1)
```

### Running the primitive with your own data

In some cases you will want to run the primitive with your own data.

In order to do so, you should pass the expected data by the primitive as
additional arguments to the `run_primitive` function. Those additional
arguments depend on the type and subtype of the primitive, and must be
passed to their respective fields:

* `amplitude_values (numpy.ndarray or None)`:
    Array of floats representing signal values or ``None``.
* `sampling_frequency (float, int or None)`:
    Sampling frequency value passed in Hz or ``None``.
* `frequency_values (numpy.ndarray or None)`:
    Array of floats representing frequency values for the given amplitude values
    or ``None``.
* `time_values (numpy.ndarray or None)`:
    Array of floats representing time values or ``None``.

Here is an example where you pass your own `amplitude_values` for the `mean`
primitive (bear in mind that this primitive only requires amplitude values
if more data was needed then it has to be passed as well):

```python=
import numpy as np

data = np.array([1, 2, 3])

run_primitive(
    'sigpro.aggregations.amplitude.statistical.mean',
    amplitude_values=data
)
```


### Passing hyperparameter values or additional context values

When a primitive accepts hyperparameters or requires additional context
values, those can be specified at the end of the `run_primitive` function.

The primitive `sigpro.aggregations.amplitude.statistical.kurtosis`
can take as input `fisher` and `bias`, both boolean values, and in order
to specify them we use `run_primitive` like this:

```python=
run_primitive(
    'sigpro.aggregations.amplitude.statistical.kurtosis',
    fisher=True,
    bias=False
)
```

This way we specified those two additional arguments for the primitive.

### Full `run_primitive` arguments list

The complete list of arguments that this function takes are as follow:

* `primitive (str)`:
    Path or name of the primitive to be used.
* `primitive_type (str)`:
    Type to which the primitive belongs to.
* `primitive_subtype (str)`:
    Subtype to which the primitive belongs to.
* `amplitude_values (numpy.ndarray or None)`:
    Array of floats representing signal values or ``None``.
* `sampling_frequency (float, int or None)`:
    Sampling frequency value passed in Hz or ``None``.
* `frequency_values (numpy.ndarray or None)`:
    Array of floats representing frequency values for the given amplitude values
    or ``None``.
* `time_values (numpy.ndarray or None)`:
    Array of floats representing time values or ``None``.
* `demo_row_index (int or None)`:
    If `int`, return the value at that index if `None` return a random index. This is used
    if no amplitude values are provided.
* `context (optional)`:
    Additional context arguments required to run the primitive.
* `hyperparameters (optional)`:
    Additional hyperparameters or tunable hyperparameters arguments.

## Creating a primitive JSON

If you need to create a primitive JSON for a new Python function that you
implemented you can use the `sigpro.contributin.make_primitive` function,
which helps you in the process.

> For complete instructions about how to write a primitive from scratch
> and contribute it to the project please read the [Contributing Guide](
> CONTRIBUTING.md)

For example, if you want to create the primitive for the implemented code
in `sigpro.aggregations.amplitude.statistical.py` for the method `mean`, you
can use:

```python=
from sigpro.contributing import make_primitive

make_primitive(
    'sigpro.aggregations.amplitude.statistical.mean'
    primitive_type='aggregation',
    primitive_subtype='amplitude',
)
```

This function will do the following steps:

* Validate that the inputs that the primitive expects are correct for its
  type and subtype.
* Validate that the function also expects the specified context arguments
  and hyperparameters.
* Validate that there are no additional arguments that have not been
  specified.
* If everything is correct, create a JSON file for your primitive in the
  `primitives` folder.


And once it finishes it will return you the absolute path where the primitive
has been stored:

```
/path/to/sigpro/primitives/aggregations/amplitude/statistical/mean.json
```

If you explore this file, you will see the primitive `json` annotation:

```json=
{
    "name": "sigpro.aggregations.amplitude.statistical.mean",
    "primitive": "sigpro.aggregations.amplitude.statistical.mean",
    "classifiers": {
        "type": "aggregation",
        "subtype": "amplitude"
    },
    "produce": {
        "args": [
            {
                "name": "amplitude_values",
                "type": "numpy.ndarray"
            }
        ],
        "output": [
            {
                "name": "value",
                "type": "float"
            }
        ]
    },
    "hyperparameters": {
        "fixed": {},
        "tunable": {}
    }
}
```

### Using your primitive path

By default, `make_primitive` will store the primitives inside the folder
`sigpro/primitives` which is located in the project. If you want to store
the primitives in a different directory you can do so by using the argument
`primitives_path`:

```python=
make_primitive(
    'sigpro.aggregations.amplitude.statistical.mean',
    primitive_type='aggregation',
    primitive_subtype='amplitude',
    primitives_path='my_primitives'
)
```

The output path now would be:

```
/path/to/my_primitives/aggregations/amplitude/statistical/mean.json
```


### Storing flat json file

If you would like to store your primtives without the path tree, you can do
so by stting the argument `primitives_subfolders` to `False`:

```python=
make_primitive(
    'sigpro.aggregations.amplitude.statistical.mean',
    primitive_type='aggregation',
    primitive_subtype='amplitude',
    primitives_path='my_primitives',
    primitives_subfolders=False,
)
```

This will create a file named `sigpro.aggregations.statistical.mean.json`
inside of the folder `my_primitives`, the contents of this `json` file
are exactly the same as the one created previously, but the nomenclature of
the file it's different, we don't have the subfolder structure.

### Creating a primitive with tunable hyperparameters

In some cases our primitives have tunable hyperparameters or fixed ones.
In order to do so you have to create a dictionary of hyperparameters with
a dictionary that contains their default value and their type (in string):

In this example you see how the `kurtosis` primitive is being created with
the tunable hyperparameters `fisher` and `bias` both being `booleans`

```python=
tunable_hyperparameters = {
    'fisher': {
        'default': True,
        'type': 'bool'
    },
    'bias': {
        'default': True,
        'type': 'bool'
    }
}

make_primitive(
    'sigpro.aggregations.amplitude.statistical.kurtosis',
    primitive_type='aggregation',
    primitive_subtype='amplitude',
    tunable_hyperparameters=tunable_hyperparameters
)
```

### Creating a primitive with context arguments

When a primitive requires of a context argument, we have to use the
argument `context_arguments` and pass it to `make_primitive`. This
argument has to be a python `list` that contains python `dictionaries`
whith the `name` and`type` of the `context_argument`.

*This is just an example of how you would pass the context argument, this
primitive does not exist.*

```python=
context_arguments = [
    {
        'name': 'test_arg1',
        'type': 'float',
    },
    {
        'name': 'test_arg2',
        'type': 'numpy.ndarray',
    },
]

make_primitive(
    'sigpro.aggregation.amplitude.context.contextual_method',
    context_arguments=context_arguments
)
```

### Full `make_primitive` arguments list

The complete list of arguments that this function takes are as follow:

* `primitive (str)`:
    The name of the primitive, the python path including the name of the
    module and the name of the function.
* `primitive_type (str)`:
    Type of primitive.
* `primitive_subtype (str)`:
    Subtype of the primitive.
* `context_arguments (list or None)`:
    A list with dictionaries containing the name and type of the context
    arguments.
* `fixed_hyperparameters (dict or None)`:
    A dictionary containing as key the name of the hyperparameter and as
    value a dictionary containing the type and the default value that it
    should take.
* `tunable_hyperparameters (dict or None)`:
    A dictionary containing as key the name of the hyperparameter and as
    value a dictionary containing the type and the default value and the
    range of values that it can take.
* `primitive_outputs (list or None)`:
    A list with dictionaries containing the name and type of the output
    values. If ``None`` default values for those will be used.
* `primitives_path (str)`:
    Path to the root of the primitives folder, in which the primitives JSON
    will be stored. Defaults to `sigpro/primitives`.
* `primitives_subfolders (bool)`:
    Whether to store the primitive JSON in a subfolder tree (``True``) or to
    use a flat primitive name (``False``). Defaults to ``True``.
