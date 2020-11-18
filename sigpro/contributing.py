"""Tools to contribute a primitive."""
from mlblocks import MLBlock
from mlblocks.discovery import load_primitive

from sigpro.demo import get_amplitude_demo, get_frequency_demo, get_frequency_time_demo

DEMO_FUNCTIONS = {
    'aggregation': {
        'amplitude': get_amplitude_demo,
        'frequency': get_frequency_demo,
        'frequency_time': get_frequency_time_demo
    },
    'transformation': {
        'amplitude': get_amplitude_demo,
        'frequency': get_amplitude_demo,
        'frequency_time': get_amplitude_demo,
    }
}

PRIMITIVE_INPUTS = {
    'transformation': {
        'amplitude': {
            'args': (
                {
                    'name': 'amplitude_values',
                    'type': 'numpy.ndarray',
                },
                {
                    'name': 'sampling_frequency',
                    'type': 'float',
                    'optional': True,
                }
            ),
            'output': (
                {
                    'name': 'amplitude_values',
                    'type': 'numpy.ndarray',
                }
            )
        },
        'frequency': {
            'args': (
                {
                    'name': 'amplitude_values',
                    'type': 'numpy.ndarray',
                },
                {
                    'name': 'sampling_frequency',
                    'type': 'float',
                }
            ),
            'output': (
                {
                    'name': 'amplitude_values',
                    'type': 'numpy.ndarray',
                },
                {
                    'name': 'frequency_values',
                    'type': 'numpy.ndarray',
                },
            )
        },
        'frequency_time': {
            'args': (
                {
                    'name': 'amplitude_values',
                    'type': 'numpy.ndarray',
                },
                {
                    'name': 'sampling_frequency',
                    'type': 'float',
                }
            ),
            'output': (
                {
                    'name': 'amplitude_values',
                    'type': 'numpy.ndarray',
                },
                {
                    'name': 'frequency_values',
                    'type': 'numpy.ndarray',
                },
            )
        },
    },
    'aggregation': {
        'amplitude': {
            'args': (
                {
                    'name': 'amplitude_values',
                    'type': 'numpy.ndarray',
                },
                {
                    'name': 'frequency_values',
                    'type': 'numpy.ndarray',
                    'optional': True,
                }
            )
        },
        'frequency': {
            'args': (
                {
                    'name': 'amplitude_values',
                    'type': 'numpy.ndarray',
                },
                {
                    'name': 'frequency_values',
                    'type': 'numpy.ndarray',
                }
            )
        },
        'frequency_time': {
            'args': (
                {
                    'name': 'amplitude_values',
                    'type': 'numpy.ndarray',
                },
                {
                    'name': 'frequency_values',
                    'type': 'numpy.ndarray',
                },
                {
                    'name': 'time_values',
                    'type': 'numpy.ndarray',
                }
            )
        },
    }
}


def _get_demo_data(primitive_type, primitive_subtype, index):
    get_demo = DEMO_FUNCTIONS[primitive_type][primitive_subtype]
    if primitive_type == 'aggregation':
        if primitive_subtype == 'amplitude':
            amplitude_values, sampling_frequency = get_demo(index)
            return {
                'amplitude_values': amplitude_values,
                'sampling_frequency': sampling_frequency,
            }

        if primitive_subtype == 'frequency':
            amplitude_values, frequency_values = get_demo(index)
            return {
                'amplitude_values': amplitude_values,
                'frequency_values': frequency_values,
            }

        amplitude_values, frequency_values, time_values = get_demo(index)
        return {
            'amplitude_values': amplitude_values,
            'frequency_values': frequency_values,
            'time_values': time_values
        }

    amplitude_values, sampling_frequency = get_demo(index)
    return {
        'amplitude_values': amplitude_values,
        'sampling_frequency': sampling_frequency
    }


def _check_primitive_type_and_subtype(primitive_type, primitive_subtype):
    subtypes = PRIMITIVE_INPUTS.get(primitive_type)
    if not subtypes:
        raise ValueError(f'Invalid primitive_type: {primitive_type}')

    primitive_inputs = subtypes.get(primitive_subtype)
    if not primitive_inputs:
        raise ValueError((
            f'Invalid primitive subtype for primitive of '
            f'type {primitive_type}: {primitive_subtype}'
        ))


def _get_primitive_instance(primitive, kwargs):
    expected_args = load_primitive(primitive).get('hyperparameters', {}).get('fixed', {})
    given_args = {
        key: value
        for key, value in kwargs.items()
        if key in expected_args
    }

    return MLBlock(primitive, **given_args)


def run_primitive(primitive, primitive_type=None, primitive_subtype=None,
                  amplitude_values=None, sampling_frequency=None,
                  frequency_values=None, time_values=None, index=None, **kwargs):
    """Run a given `primitive` with the specified configuration.

    Given a primitive and it's hyperparameters, attempt to run this against either the data
    provided by the user or against the demo data. If there is no data provided, the type
    and subtype of the primitive must be passed as arguments if those are not specified inside
    the metadata. If the data it's passed for the primitive there is no requirement of the type
    and subtype.

    In order to validate the primitive this function will run the following steps:

        * Create an instance of the primitive.
        * Call the primitive for each row in the data (the provided by the user or the demo)
          using the given hyperparameter values.
        * Return a list of tuples with the output that the primitive generated

    Args:
        primitive (str):
            Path or name of the primitive to be used.
        primitive_type (str):
            Type to which the primitive belongs to.
        primitive_subtype (str):
            Subtype to which the primitive belongs to.
        amplitude_values (numpy.ndarray or None):
            Array of floats representing signal values or ``None``.
        sampling_frequency (float, int or None):
            Sampling frequency value passed in Hz or ``None``.
        frequency_values (numpy.ndarray or None):
            Array of floats representing frequency values for the given amplitude values
            or ``None``.
        time_values (numpy.ndarray or None):
            Array of floats representing time values or ``None``.
        index (int or None):
            If `int`, return the value at that index if `None` return a random index. This is used
            if no amplitude values is provided in order to retrieve data from the demo.
        context (optional):
            Additional context arguments required to run the primitive.
        hyperparameters (optional):
            Additional hyperparameters or tunable hyperparameters arguments.

    Returns:
        tuple:
            A tuple with the produced values from the primitive for each row of the demo data
            corresponding to the type and subtype of this.
    """
    primitive = _get_primitive_instance(primitive, kwargs)

    if amplitude_values is not None:
        data = {
            'amplitude_values': amplitude_values,
            'sampling_frequency': sampling_frequency,
            'frequency_values': frequency_values,
            'time_values': time_values,
        }

    else:
        if primitive_type is None:
            primitive_type = primitive.metadata['classifiers']['type']
            primitive_subtype = primitive.metadata['classifiers']['subtype']

        _check_primitive_type_and_subtype(primitive_type, primitive_subtype)
        data = _get_demo_data(primitive_type, primitive_subtype, index=index)

    kwargs.update(data)
    return primitive.produce(**kwargs)
