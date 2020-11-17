"""Tools to contribute a primitive."""
import numpy as np
import scipy.signal

from sigpro.demo import get_demo_data

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


def _check_primitive_type_and_subtype(primitive_type, primitive_subtype):
    subtypes = PRIMITIVE_INPUTS.get(primitive_type)
    if not subtypes:
        raise ValueError(f'Invalid primitive_type: {primitive_type}')

    primitive_inputs = subtypes.get(primitive_subtype)
    if not primitive_inputs:
        raise ValueError((
            f'Invalid primitive subtype for primitive of '
            'type {primitive_type}: {primitive_subtype}'
        ))

def _get_demo_data(primitive_type, primitive_subtype):
    demo_data = get_demo_data()
    if primitive_type == 'aggregation':
        if primitive_subtype == 'frequency_time':
            demo_data = demo_data['values'].apply(scipy.signal.stft, fs=10000)

            # TODO: Extract and separate amplitude values, frequency values and time values
            # return {
            #     'amplitude_values': amplitude_values,
            #     'frequency_values': frequency_values,
            #     'time_values': time_values
            # }

        else:
            demo_data = get_demo_data()
            demo_data = demo_data['values'].apply(np.fft.fft)
            amplitude_values = demo_data.apply(np.real)
            # 10000 is the sampling frequency used in the demo data
            frequency_values = np.fft.fftfreq(len(amplitude_values), 10000)
            return {
                'amplitude_values': amplitude_values,
                'frequency_values': frequency_values
            }

    if primitive_type == 'transformation':
        demo_data = get_demo_data()
        demo_data = demo_data['values']
        amplitude_values = demo_data.apply(np.real)
        # 10000 is the sampling frequency used in the demo data
        sampling_frequency = 10000
        return {
            'amplitude_values': amplitude_values,
            'sampling_frequency': sampling_frequency
        }


def run_primitive(primitive, primitive_type=None, primitive_subtype=None,
                  amplitude_values=None, sampling_frequency=None,
                  frequency_values=None, time_values=None, **kwargs):
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
        context (optional):
            Additional context arguments required to run the primitive.
        hyperparameters (optional):
            Additional hyperparameters or tunable hyperparameters arguments.

    Returns:
        tuple:
            A tuple with the produced values from the primitive for each row of the demo data
            corresponding to the type and subtype of this.
    """
    primitive = MLBlocks(primitive)
    data = None

    if amplitude_values:
        data = {
            'amplitude_values': amplitude_values,
            'sampling_frequency': sampling_frequency,
            'frequency_values': frequency_values,
            'time_values': time_values,
        }

    else:
        if primitive_type is None:
            primitive_type = primitive.metadata['classifiers'].get('type')
            primitive_subtype = primitive.metadata['classifiers'].get('subtype')

        _check_primitive_type_and_subtype(primitive_type, primitive_subtype)
        data = _get_demo_data(primitive_type, primitive_subtype)

    primitive_args = {}
    primitive_produce_args = primitive.produce_args.copy()
    primitive_produce_args = [item['name'] for item in primitive_produce_args]
    data_args = [name for name in data.keys() if name in primitive_produce_args]
    produce_args_names = [name for name in kwargs]

    missing = list(set(primitive_produce_args).difference(produce_args_names + data_args))
    if missing:
        raise ValueError(f'Required args by the primitive not found: {missing}')
