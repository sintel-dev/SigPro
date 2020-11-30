"""Tools to contribute a primitive."""
import importlib
import inspect
import json
import os

from mlblocks import MLBlock
from mlblocks.discovery import load_primitive

from sigpro.demo import get_amplitude_demo, get_frequency_demo, get_frequency_time_demo

DEMO_FUNCTIONS = {
    'aggregation': {
        'amplitude': (get_amplitude_demo, 'amplitude_values', 'sampling_frequency'),
        'frequency': (get_frequency_demo, 'amplitude_values', 'frequency_values'),
        'frequency_time': (
            get_frequency_time_demo, 'amplitude_values', 'frequency_values', 'time_values'),
    },
    'transformation': {
        'amplitude': (get_amplitude_demo, 'amplitude_values', 'sampling_frequency'),
        'frequency': (get_amplitude_demo, 'amplitude_values', 'sampling_frequency'),
        'frequency_time': (get_amplitude_demo, 'amplitude_values', 'sampling_frequency'),
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
                },
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
            ),
            'output': (
                {
                    'name': 'value',
                    'type': 'float',
                },
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
            ),
            'output': (
                {
                    'name': 'value',
                    'type': 'float',
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
                    'name': 'frequency_values',
                    'type': 'numpy.ndarray',
                },
                {
                    'name': 'time_values',
                    'type': 'numpy.ndarray',
                }
            ),
            'output': (
                {
                    'name': 'value',
                    'type': 'float',
                },
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


def _import_object(object_name):
    """Import an object from its Fully Qualified Name."""
    try:
        package, name = object_name.rsplit('.', 1)
        return getattr(importlib.import_module(package), name)
    except (AttributeError, ModuleNotFoundError, ValueError):
        raise ImportError(f'Cannot import {object_name}') from None


def _validate_subtype_inputs(function_args, primitive_inputs):
    for primitive_input in primitive_inputs:
        arg_name = primitive_input['name']
        optional = primitive_input.get('optional')
        if optional:
            arg_name = arg_name[1:]
        elif arg_name not in function_args:
            raise ValueError(f'Primitive does not have `{arg_name}` argument (primitive type)')

        if arg_name in function_args:
            function_args.remove(arg_name)
            yield {
                'name': arg_name,
                'type': primitive_input['type']
            }


def _validate_context_arguments(function_args, context_arguments):
    for context_argument in context_arguments:
        arg_name = context_argument['name']
        if arg_name not in function_args:
            raise ValueError(f'Primitive does not have `{arg_name}` argument (context)')

        function_args.remove(arg_name)
        yield {
            'name': arg_name,
            'type': context_argument['type']
        }


def _validate_hyperparameters(function_args, hyperparameters):
    for name in hyperparameters.keys():
        if name not in function_args:
            raise ValueError(f'Primitive does not have `{name}` argument (hyperparameter)')

        function_args.remove(name)


def _get_primitive_args(primitive_function, primitive_inputs, context_arguments,
                        fixed_hyperparameters, tunable_hyperparameters):
    argspec = inspect.getfullargspec(primitive_function)
    function_args = argspec.args.copy()
    primitive_args = []

    primitive_args.extend(_validate_subtype_inputs(function_args, primitive_inputs))
    primitive_args.extend(_validate_context_arguments(function_args, context_arguments))
    _validate_hyperparameters(function_args, fixed_hyperparameters)
    _validate_hyperparameters(function_args, tunable_hyperparameters)

    if function_args:
        raise ValueError(f'Unexpected additional arguments found: {function_args}')

    return primitive_args


def _get_primitive_spec(primitive_type, primitive_subtype):

    subtypes = PRIMITIVE_INPUTS.get(primitive_type)
    if not subtypes:
        raise ValueError(f'Invalid primitive_type: {primitive_type}')

    primitive_spec = subtypes.get(primitive_subtype)
    if not primitive_spec:
        raise ValueError((
            f'Invalid primitive_subtype for primitive of '
            f'type {primitive_type}: {primitive_subtype}'
        ))

    return primitive_spec


def _write_primitive(primitive_dict, primitive_name, primitives_path, primitives_subfolders):
    primitives_path = os.path.abspath(primitives_path)

    if primitives_subfolders:
        output_path = primitive_name.split('.')
        file_name = f'{output_path.pop()}.json'
        output_path = os.path.join(primitives_path, *output_path)
        os.makedirs(output_path, exist_ok=True)
        primitive_path = os.path.join(output_path, file_name)

    else:
        file_name = f'{primitive_name}.json'
        primitive_path = os.path.join(primitives_path, file_name)

    with open(primitive_path, 'w') as primitive_file:
        json.dump(primitive_dict, primitive_file, indent=4)

    return primitive_path


def make_primitive(primitive, primitive_type, primitive_subtype,
                   context_arguments=None, fixed_hyperparameters=None,
                   tunable_hyperparameters=None, primitive_outputs=None,
                   primitives_path='sigpro/primitives', primitives_subfolders=True):
    """Create a primitive JSON.

    During the JSON creation the primitive function signature is validated to
    ensure that it matches the primitive type and subtype implicitly specified
    by the primitive name.

    Any additional function arguments are also validated to ensure that the
    function does actually expect them.

    Args:
        primitive (str):
            The name of the primitive, the python path including the name of the
            module and the name of the function.
        primitive_type (str):
            Type of primitive.
        primitive_subtype (str):
            Subtype of the primitive.
        context_arguments (list or None):
            A list with dictionaries containing the name and type of the context arguments.
        fixed_hyperparameters (dict or None):
            A dictionary containing as key the name of the hyperparameter and as
            value a dictionary containing the type and the default value that it
            should take.
        tunable_hyperparameters (dict or None):
            A dictionary containing as key the name of the hyperparameter and as
            value a dictionary containing the type and the default value and the
            range of values that it can take.
        primitive_outputs (list or None):
            A list with dictionaries containing the name and type of the output values. If
            ``None`` default values for those will be used.
        primitives_path (str):
            Path to the root of the primitives folder, in which the primitives JSON will be stored.
            Defaults to `sigpro/primitives`.
        primitives_subfolders (bool):
            Whether to store the primitive JSON in a subfolder tree (``True``) or to use a flat
            primitive name (``False``). Defaults to ``True``.

    Raises:
        ValueError:
            If the primitive specification arguments are not valid.

    Returns:
        str:
            Path of the generated JSON file.
    """
    context_arguments = context_arguments or []
    fixed_hyperparameters = fixed_hyperparameters or {}
    tunable_hyperparameters = tunable_hyperparameters or {}

    primitive_spec = _get_primitive_spec(primitive_type, primitive_subtype)
    primitive_inputs = primitive_spec['args']
    primitive_outputs = primitive_outputs or primitive_spec['output']

    primitive_function = _import_object(primitive)
    primitive_args = _get_primitive_args(
        primitive_function,
        primitive_inputs,
        context_arguments,
        fixed_hyperparameters,
        tunable_hyperparameters
    )

    primitive_dict = {
        'name': primitive,
        'primitive': primitive,
        'classifiers': {
            'type': primitive_type,
            'subtype': primitive_subtype
        },
        'produce': {
            'args': primitive_args,
            'output': [
                {
                    'name': primitive_output['name'],
                    'type': primitive_output['type'],
                }
                for primitive_output in primitive_outputs
            ],
        },
        'hyperparameters': {
            'fixed': fixed_hyperparameters,
            'tunable': tunable_hyperparameters
        }
    }

    return _write_primitive(primitive_dict, primitive, primitives_path, primitives_subfolders)


def run_primitive(primitive, primitive_type=None, primitive_subtype=None,
                  amplitude_values=None, sampling_frequency=None,
                  frequency_values=None, time_values=None, demo_row_index=None, **kwargs):
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
        demo_row_index (int or None):
            If `int`, return the value at that index if `None` return a random index. This is used
            if no amplitude values are provided.
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
        get_demo_data_function, *arg_names = DEMO_FUNCTIONS[primitive_type][primitive_subtype]
        data = dict(zip(arg_names, get_demo_data_function(index=demo_row_index)))

    kwargs.update(data)
    return primitive.produce(**kwargs)
