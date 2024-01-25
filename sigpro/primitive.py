# -*- coding: utf-8 -*-
"""SigPro Primitive class."""

import copy

from mlblocks.mlblock import import_object

from sigpro.contributing import (
    _check_primitive_type_and_subtype, _get_primitive_args, _get_primitive_spec,
    _make_primitive_dict, _write_primitive)


class Primitive():  # pylint: disable=too-many-instance-attributes
    """
    Represents a SigPro primitive.

    Each primitive object represents a specific transformation or aggregation. Moreover,
    a Primitive maintains all the information in its JSON annotation as well as its
    hyperparameter values.

    Args:
        primitive (str):
            The name of the primitive, the python path including the name of the
            module and the name of the function.
        primitive_type (str):
            Type of primitive.
        primitive_subtype (str):
            Subtype of the primitive.
        init_params (dict):
            Initial (fixed) hyperparameter values of the primitive in
            {hyperparam_name: hyperparam_value} format.
    """

    def __init__(self, primitive, primitive_type, primitive_subtype, init_params=None):

        self.primitive = primitive
        self.tag = primitive.split('.')[-1]
        self.primitive_type = primitive_type
        self.primitive_subtype = primitive_subtype
        self.tunable_hyperparameters = {}
        self.fixed_hyperparameters = {}
        self.context_arguments = []
        primitive_spec = _get_primitive_spec(primitive_type, primitive_subtype)
        self.primitive_inputs = primitive_spec['args']
        self.primitive_outputs = primitive_spec['output']

        _check_primitive_type_and_subtype(primitive_type, primitive_subtype)

        self.primitive_function = import_object(primitive)
        if init_params is None:
            init_params = {}
        self.hyperparameter_values = init_params

    def get_name(self):
        """Get the name of the primitive."""
        return self.primitive

    def get_tag(self):
        """Get the tag of the primitive."""
        return self.tag

    def get_inputs(self):
        """Get the inputs of the primitive."""
        return copy.deepcopy(self.primitive_inputs)

    def get_outputs(self):
        """Get the outputs of the primitive."""
        return copy.deepcopy(self.primitive_outputs)

    def get_type_subtype(self):
        """Get the type and subtype of the primitive."""
        return self.primitive_type, self.primitive_subtype

    def get_context_arguments(self):
        """Get the context arguments of the primitive."""
        return copy.deepcopy(self.context_arguments)

    def _validate_primitive_spec(self):  # check compatibility of given parameters.
        _get_primitive_args(
            self.primitive_function,
            self.primitive_inputs,
            self.context_arguments,
            self.fixed_hyperparameters,
            self.tunable_hyperparameters)

    def get_hyperparam_dict(self):
        """Return the dictionary of fixed hyperparameters for use in Pipelines."""
        return {'name': self.get_tag(), 'primitive': self.get_name(),
                'init_params': copy.deepcopy(self.hyperparameter_values)}

    def set_tag(self, tag):
        """Set the tag of a primitive."""
        self.tag = tag
        return self

    def set_primitive_inputs(self, primitive_inputs):
        """Set primitive inputs."""
        self.primitive_inputs = primitive_inputs

    def set_primitive_outputs(self, primitive_outputs):
        """Set primitive outputs."""
        self.primitive_outputs = primitive_outputs

    def _set_primitive_type(self, primitive_type):
        self.primitive_type = primitive_type

    def _set_primitive_subtype(self, primitive_subtype):
        self.primitive_subtype = primitive_subtype

    def set_context_arguments(self, context_arguments):
        """Set context_arguments of a primitive."""
        self.context_arguments = context_arguments

    def set_tunable_hyperparameters(self, tunable_hyperparameters):
        """Set tunable hyperparameters of a primitive."""
        self.tunable_hyperparameters = tunable_hyperparameters

    def set_fixed_hyperparameters(self, fixed_hyperparameters):
        """Set fixed hyperparameters of a primitive."""
        self.fixed_hyperparameters = fixed_hyperparameters

    def make_primitive_json(self):
        """
        View the primitive json produced by a Primitive object.

        Raises:
            ValueError:
                If the primitive specification arguments are not valid (as in sigpro.contributing).
        Returns:
            dict:
                Dictionary containing the JSON annotation for the primitive.
        """
        self._validate_primitive_spec()
        return _make_primitive_dict(self.primitive, self.primitive_type,
                                    self.primitive_subtype, self.context_arguments,
                                    self.fixed_hyperparameters, self.tunable_hyperparameters,
                                    self.primitive_inputs, self.primitive_outputs)

    def write_primitive_json(self, primitives_path='sigpro/primitives',
                             primitives_subfolders=True):
        """
        Write the primitive json produced by a Primitive object and return the path.

        Args:
            primitives_path (str):
                Path to the root of the primitives folder, in which the primitives JSON will be
                stored. Defaults to `sigpro/primitives`.
            primitives_subfolders (bool):
                Whether to store the primitive JSON in a subfolder tree (``True``) or to use a flat
                primitive name (``False``). Defaults to ``True``.

        Returns:
            str:
                Path of the generated JSON file.
        """
        return _write_primitive(self.make_primitive_json(), self.primitive,
                                primitives_path, primitives_subfolders)

# Primitive inheritance subclasses
# pylint: disable=super-init-not-called
# Transformations


class TransformationPrimitive(Primitive):
    """Generic transformation primitive."""

    def __init__(self, primitive, primitive_subtype, init_params=None):
        super().__init__(primitive, 'transformation', primitive_subtype, init_params=init_params)


class AmplitudeTransformation(TransformationPrimitive):
    """Generic amplitude transformation primitive."""

    def __init__(self, primitive, init_params=None):
        super().__init__(primitive, 'amplitude', init_params=init_params)


class FrequencyTransformation(TransformationPrimitive):
    """Generic frequency transformation primitive."""

    def __init__(self, primitive, init_params=None):
        super().__init__(primitive, 'frequency', init_params=init_params)


class FrequencyTimeTransformation(TransformationPrimitive):
    """Generic frequency-time transformation primitive."""

    def __init__(self, primitive, init_params=None):
        super().__init__(primitive, 'frequency_time', init_params=init_params)


class ComparativeTransformation(TransformationPrimitive):
    """Generic comparative transformation primitive."""

    def __init__(self, primitive, init_params=None):
        raise NotImplementedError
# Aggregations


class AggregationPrimitive(Primitive):
    """Generic aggregation primitive."""

    def __init__(self, primitive, primitive_subtype, init_params=None):
        super().__init__(primitive, 'aggregation', primitive_subtype, init_params=init_params)


class AmplitudeAggregation(AggregationPrimitive):
    """Generic amplitude aggregation primitive."""

    def __init__(self, primitive, init_params=None):
        super().__init__(primitive, 'amplitude', init_params=init_params)


class FrequencyAggregation(AggregationPrimitive):
    """Generic frequency aggregation primitive."""

    def __init__(self, primitive, init_params=None):
        super().__init__(primitive, 'frequency', init_params=init_params)


class FrequencyTimeAggregation(AggregationPrimitive):
    """Generic frequency-time aggregation primitive."""

    def __init__(self, primitive, init_params=None):
        super().__init__(primitive, 'frequency_time', init_params=init_params)


class ComparativeAggregation(AggregationPrimitive):
    """Generic comparative aggregation primitive."""

    def __init__(self, primitive, init_params=None):
        raise NotImplementedError
