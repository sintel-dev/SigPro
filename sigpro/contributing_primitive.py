"""Contributing primitive classes"""
import copy
from sigpro.contributing import make_primitive
from sigpro.primitive import FrequencyTransformation, AmplitudeTransformation, FrequencyTimeTransformation
from sigpro.primitive import FrequencyAggregation, AmplitudeAggregation, FrequencyTimeAggregation 

TAXONOMY =  { 
    'transformation' : {
        'frequency' : FrequencyTransformation,
        'amplitude' : AmplitudeTransformation,
        'frequency_time': FrequencyTimeTransformation,
    }, 'aggregation' : {
        'frequency' : FrequencyAggregation,
        'amplitude' : AmplitudeAggregation,
        'frequency_time': FrequencyTimeAggregation,
    }
}

def get_primitive_class(primitive, primitive_type, primitive_subtype,
                   context_arguments=None, fixed_hyperparameters=None,
                   tunable_hyperparameters=None, primitive_outputs=None):
    """ Get a dynamically generated primitive class.

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
    Raises:
        ValueError:
            If the primitive specification arguments are not valid.

    Returns:
        type:
            Dynamically-generated custom Primitive type.
    """
    primitive_type_class = TAXONOMY[primitive_type][primitive_subtype]
    class UserPrimitive(primitive_type_class):
        def __init__(self, **kwargs):
            init_params = {}
            if fixed_hyperparameters is not None:
                init_params = { param: kwargs[param] for param in fixed_hyperparameters}
            super().__init__(primitive, init_params =  init_params)
            if fixed_hyperparameters is not None:
                self.set_fixed_hyperparameters(copy.deepcopy(fixed_hyperparameters))
            if tunable_hyperparameters is not None:
                self.set_tunable_hyperparameters(copy.deepcopy(tunable_hyperparameters))
            if primitive_outputs is not None:
                self.set_primitive_outputs(copy.deepcopy(primitive_outputs))
            if context_arguments is not None:
                self.set_context_arguments(copy.deepcopy(context_argments))

    type_name = f'Custom_{primitive}'

    return type(type_name, ( UserPrimitive, ), {})


def make_primitive_class(primitive, primitive_type, primitive_subtype,
                   context_arguments=None, fixed_hyperparameters=None,
                   tunable_hyperparameters=None, primitive_outputs=None,
                   primitives_path='sigpro/primitives', primitives_subfolders=True):
    """ Get a dynamically generated primitive class and make the primitive JSON.
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
        type:
            Dynamically-generated custom Primitive type.
        str:
            Path of the generated JSON file.
    """
    return get_primitive_class(primitive, primitive_type, primitive_subtype,
                   context_arguments, fixed_hyperparameters,
                   tunable_hyperparameters, primitive_outputs), make_primitive(primitive,
                   primitive_type, primitive_subtype,
                   context_arguments, fixed_hyperparameters,
                   tunable_hyperparameters, primitive_outputs,
                   primitives_path, primitives_subfolders)
