# -*- coding: utf-8 -*-
"""Pipeline signal processing functionality."""

from abc import ABC
from collections import Counter
from copy import copy, deepcopy
from itertools import product

import pandas as pd
from mlblocks import MLPipeline

# from mlblocks.mlblock import import_object
# from sigpro import contributing, primitive
from sigpro.primitive import Primitive

# Temporary refactor from core, ignore duplicate code.
# pylint: disable = duplicate-code, too-many-statements, too-many-nested-blocks

DEFAULT_INPUT = [
    {
        'name': 'readings',
        'keyword': 'data',
        'type': 'pandas.DataFrame'
    },
    {
        'name': 'feature_columns',
        'default': None,
        'type': 'list'
    }
]

DEFAULT_OUTPUT = [
    {
        'name': 'readings',
        'type': 'pandas.DataFrame'
    },
    {
        'name': 'feature_columns',
        'type': 'list'
    }
]


class Pipeline(ABC):
    """Abstract Pipeline class to apply multiple transformation and aggregation primitives."""

    def __init__(self):
        self.values_column_name = 'values'
        self.input_is_dataframe = True
        self.pipeline = None

    def get_pipeline(self):
        """Return the MLPipeline in self.pipeline."""
        return self.pipeline

    def _set_values_column_name(self, values_column_name):
        self.values_column_name = values_column_name

    def _accept_dataframe_input(self, input_is_dataframe):
        self.input_is_dataframe = input_is_dataframe

    def _apply_pipeline(self, window, is_series=False):
        """Apply a ``mlblocks.MLPipeline`` to a row.

        Apply a ``MLPipeline`` to a window of a ``pd.DataFrame``, this function can
        be combined with the ``pd.DataFrame.apply`` method to be applied to the
        entire data frame.

        Args:
            window (pd.Series):
                Row or multiple rows (window) used to apply the pipeline to.
            is_series (bool):
                Indicator whether window is formated as a series or dataframe.
        """
        if is_series:
            context = window.to_dict()
            amplitude_values = context.pop(self.values_column_name)
        else:
            context = {} if window.empty else {
                k: v for k, v in window.iloc[0].to_dict().items() if k != self.values_column_name
            }
            amplitude_values = list(window[self.values_column_name])
        output = self.pipeline.predict(
            amplitude_values=amplitude_values,
            **context,
        )
        output_names = self.pipeline.get_output_names()

        # ensure that we can iterate over output
        output = output if isinstance(output, tuple) else (output, )

        return pd.Series(dict(zip(output_names, output)))

    def get_primitives(self):
        """Get a list of primitives in the pipeline."""
        raise NotImplementedError

    def get_output_features(self):
        """Get a list of output feature tuples produced by the pipeline."""
        raise NotImplementedError

    def process_signal(self, data=None, window=None, values_column_name='values',
                       time_index=None, groupby_index=None, feature_columns=None,
                       keep_columns=False, input_is_dataframe=True, **kwargs):
        """Apply multiple transformation and aggregation primitives.

        The process_signals method is responsible for applying a Pipeline specified by the
        user in order to create features for the given data.

        Args:
            data (pandas.DataFrame):
                Dataframe with a column that contains signal values.
            window (str):
                Duration of window size, e.g. ('1h').
            values_column_name (str):
                Column in ``data`` that represents the signal values.
            time_index (str):
                Column in ``data`` that represents the time index.
            groupby_index (str or list[str]):
                Column(s) to group together and take the window over.
            feature_columns (list):
                List of column names from the input data frame that must be considered as
                features and should not be dropped.
            keep_columns (Union[bool, list]):
                Whether to keep non-feature columns in the output DataFrame or not.
                If a list of column names are passed, those columns are kept.
            input_is_dataframe (bool):
                Whether the input data is a Dataframe. Used for MLBlocks integration.
        Returns:
            tuple:
                pandas.DataFrame:
                    A data frame with new feature columns by applying the previous primitives. If
                    ``keep_columns`` is ``True`` the original signal values and non-feature
                    columns will be conserved in the data frame, otherwise any columns
                    not named in ``keep_columns`` will be deleted.
                list:
                    A list with the feature names generated.
        """
        # Error messages are hard to interpret.
        self._set_values_column_name(values_column_name)
        self._accept_dataframe_input(input_is_dataframe)

        if data is None:
            window = pd.Series(kwargs)
            values = self._apply_pipeline(window, is_series=True).values
            return values if len(values) > 1 else values[0]

        data = data.copy()
        if window is not None and groupby_index is not None:
            features = data.set_index(time_index).groupby(groupby_index).resample(
                rule=window, **kwargs).apply(
                self._apply_pipeline
            ).reset_index()
            data = features

        else:
            features = data.apply(
                self._apply_pipeline,
                axis=1,
                is_series=True
            )
            data = pd.concat([data, features], axis=1)

        if feature_columns:
            feature_columns = feature_columns + list(features.columns)
        else:
            feature_columns = list(features.columns)

        if isinstance(keep_columns, list):
            data = data[keep_columns + feature_columns]
        elif not keep_columns:
            data = data[feature_columns]

        return data, feature_columns

    def get_input_args(self):
        """Return the pipeline input args."""
        if self.input_is_dataframe:
            return deepcopy(DEFAULT_INPUT)

        return self.pipeline.get_predict_args()

    def get_output_args(self):
        """Return the pipeline output args."""
        if self.input_is_dataframe:
            return deepcopy(DEFAULT_OUTPUT)

        return self.pipeline.get_outputs()


class LinearPipeline(Pipeline):
    """
    LinearPipeline class applies multiple transformation and aggregation primitives.

    The LinearPipeline class applies a sequence of transformation primitives and applies several
    aggregation primitives in parallel to produce output features.

    Args:
        transformations (list):
            List of transformation primitive objects.
        aggregations (list):
            List of dictionaries containing the aggregation primitives.
    """

    def __init__(self, transformations, aggregations):  # pylint: disable=too-many-locals

        super().__init__()
        self.transformations = transformations
        self.aggregations = aggregations

        primitives = []
        init_params = {}
        prefix = []
        outputs = []
        counter = Counter()

        for transformation_ in self.transformations:
            transformation_._validate_primitive_spec()
            transformation = transformation_.get_hyperparam_dict()

            name = transformation.get('name')
            if name is None:
                name = transformation['primitive'].split('.')[-1]

            prefix.append(name)
            primitive = transformation['primitive']
            counter[primitive] += 1
            primitive_name = f'{primitive}#{counter[primitive]}'
            primitives.append(primitive)
            params = transformation.get('init_params')
            if params:
                init_params[primitive_name] = params

        prefix = '.'.join(prefix) if prefix else ''

        for aggregation_ in self.aggregations:
            aggregation_._validate_primitive_spec()
            aggregation = aggregation_.get_hyperparam_dict()

            name = aggregation.get('name')
            if name is None:
                name = aggregation['primitive'].split('.')[-1]

            aggregation_name = f'{prefix}.{name}' if prefix else name

            primitive = aggregation['primitive']
            counter[primitive] += 1
            primitive_name = f'{primitive}#{counter[primitive]}'
            primitives.append(primitive)

            primitive = aggregation_.make_primitive_json()
            primitive_outputs = primitive['produce']['output']

            params = aggregation.get('init_params')
            if params:
                init_params[primitive_name] = params

            if name.lower() == 'sigpro':
                primitive = MLPipeline([primitive], init_params={'sigpro.SigPro#1': params})
                primitive_outputs = primitive.get_outputs()

            if not isinstance(primitive_outputs, str):
                for output in primitive_outputs:
                    output = output['name']
                    outputs.append({
                        'name': f'{aggregation_name}.{output}',
                        'variable': f'{primitive_name}.{output}'
                    })

        outputs = {'default': outputs} if outputs else None

        self.pipeline = MLPipeline(
            primitives,
            init_params=init_params,
            outputs=outputs)

    def get_primitives(self):
        """Get a list of primitives in the pipeline."""
        return copy(self.transformations.copy() + self.aggregations.copy())

    def get_output_features(self):
        """Get a list of output feature tuples produced by the pipeline."""
        return [tuple(self.transformations.copy() + [aggregation])
                for aggregation in self.aggregations]


def build_linear_pipeline(transformations, aggregations):
    """
    Build a linear pipeline with given transformation and aggregation layers.

    Args:
        transformations (list): List of transformation primitives.

        aggregations (list): List of aggregation primitives.

    Returns:
        sigpro.pipeline.LinearPipeline:
            A ``LinearPipeline`` object that produces the features from applying each
            aggregation individually to the result of applying all transformations to
            the input data.
    """
    pipeline_object = LinearPipeline(transformations, aggregations)
    return pipeline_object


class LayerPipeline(Pipeline):
    """
    Layer pipelines in SigPro.

    Args:
        primitives (list): List of primitive objects. All primitives should have distinct tags.

        primitive_combinations (list): List of output features to be generated. Each feature
            in primitive_combinations should be a tuple of primitive objects found as keys in
            primitives, or a tuple of their string tags. All combinations should start w/ some
            (possibly zero) number of transformations and end with a single aggregation.

        features_as_strings (bool): True if primitive_combinations is defined w/ string names,
        False if primitive_combinations is defined with primitive objects (default).

    Returns:
        LayerPipeline that generates the primitives in primitive_combinations.
    """

    def __init__(self, primitives, primitive_combinations, features_as_strings=False):
        """Initialize a LayerPipeline."""
        super().__init__()
        if not isinstance(primitives, list):
            raise ValueError('primitives must a list')
        primitives_dict = {}
        for primitive in primitives:
            if not isinstance(primitive, Primitive):
                raise ValueError('Non-primitive specified in list primitives')

            if primitive.get_tag() in primitives_dict:
                raise ValueError(f'Tag {primitive.get_tag()} duplicated in \
                                    list primitives. All primitives must have distinct tags.')

            primitives_dict[primitive.get_tag()] = primitive
        self.primitives = copy(primitives[:])
        self.primitive_combinations = None

        if features_as_strings:
            primitive_combinations = [tuple(primitives_dict[tag] for tag in tag_tuple)
                                      for tag_tuple in primitive_combinations]

        self.primitive_combinations = [tuple(combination) for combination
                                       in primitive_combinations]

        length = max([len(combination) for combination in primitive_combinations] + [0])

        if length == 0:
            raise ValueError('At least one non-empty output feature must be specified')
        self.num_layers = length

        for combination in self.primitive_combinations:

            combo_length = len(combination)
            for ind in range(combo_length - 1):
                if combination[ind].get_type_subtype()[0] != 'transformation':
                    raise ValueError(f'Primitive at non-terminal position #{ind+1}/{combo_length} \
                                     is not a transformation')

            if combination[-1].get_type_subtype()[0] != 'aggregation':
                raise ValueError('Last primitive is not an aggregation')

            for primitive in combination:
                if primitive not in self.primitives:
                    raise ValueError(f'Primitive with tag {primitive.get_tag()} not found in the \
                                     given primitives')

        self.pipeline = self._build_pipeline()

    def _build_pipeline(self):  # pylint: disable=too-many-locals, too-many-branches
        """
        Build the layer pipeline.

        Returns:
            mlblocks.MLPipeline:
                An ``MLPipeline`` object that produces the features in primitives_combinations.
        """
        prefixes = {}
        primitive_counter = Counter()
        final_primitives_list = []
        final_init_params = {}
        final_primitive_inputs = {}
        final_primitive_outputs = {}
        final_outputs = []

        for layer in range(1, 1 + self.num_layers):
            for combination in self.primitive_combinations:
                combination_length = len(combination)
                if layer > combination_length:
                    continue

                if (tuple(combination[:layer]) not in prefixes) or layer == combination_length:
                    # Since all features are T.T...T.A, no combo should be a prefix of another.
                    if layer == combination_length:
                        assert tuple(combination[:layer]) not in prefixes

                    final_primitive = combination[layer - 1]
                    final_primitive_str = final_primitive.get_tag()

                    prefixes[(tuple(combination[:layer]))] = final_primitive

                    final_primitive_name = final_primitive.get_name()
                    final_primitives_list.append(final_primitive.get_name())
                    primitive_counter[final_primitive_name] += 1
                    numbered_primitive_name = \
                        f'{final_primitive_name}#{primitive_counter[final_primitive_name]}'

                    final_init_params[numbered_primitive_name] = \
                        final_primitive.get_hyperparam_dict()['init_params']

                    # Map primitive inputs and outputs.

                    final_primitive_inputs[numbered_primitive_name] = {}
                    final_primitive_outputs[numbered_primitive_name] = {}

                    for input_dict in final_primitive.get_inputs():
                        final_primitive_inputs[numbered_primitive_name][input_dict['name']] = \
                            f'{final_primitive_str}.' + str(input_dict['name'])
                        in_name = input_dict['name']
                        if 'optional' in input_dict:
                            is_required = not input_dict['optional']
                        else:
                            is_required = True
                        # Context arguments should be named properly in the input data.
                        if in_name not in final_primitive.get_context_arguments() and \
                                in_name != 'amplitude_values' and is_required:
                            # We need to hook up the primitive input to the proper output in chain
                            if layer == 1:
                                npn = numbered_primitive_name[:]  # lint
                                final_primitive_inputs[npn][in_name] = str(in_name)
                                continue
                            prev_prim = None
                            prev_ind = None

                            # Approach: find the most recent predecessor primitive in the feature
                            # that could have generated the specific input_name.

                            for p in reversed(range(0, layer)):  # pylint: disable=invalid-name
                                prev_prim_cand = combination[p - 1]
                                test_ops = [op['name'] for op in prev_prim_cand.get_outputs()]
                                if in_name in test_ops:
                                    prev_prim = prev_prim_cand
                                    prev_ind = p
                                    break

                            if prev_prim is None and layer > 1:
                                # If we can't find the predecessor, assume that the value is given.

                                final_primitive_inputs[numbered_primitive_name][in_name] = \
                                    f'{final_primitive_str}.' + str(in_name)
                                # warn user?
                                # fps = final_primitive_str  # lint
                                # raise ValueError(f'Arg {in_name} of primitive {fps} \
                                # not produced by any predecessor primitive.')
                            else:
                                clpi = combination[:prev_ind]
                                icn = '.'.join([pr.get_tag() for pr in clpi]) + f'.{prev_ind}'
                                final_primitive_inputs[numbered_primitive_name][in_name] = \
                                    f'{icn}.{in_name}'

                    if layer == 1:
                        final_primitive_inputs[numbered_primitive_name]['amplitude_values'] = \
                            'amplitude_values'
                    else:
                        clm1 = combination[:layer - 1]  # lint character limit
                        input_column_name = '.'.join([pr.get_tag() for pr in clm1]) \
                            + f'.{layer-1}'
                        final_primitive_inputs[numbered_primitive_name]['amplitude_values'] = \
                            input_column_name + '.amplitude_values'

                    output_column_name = '.'.join([prim.get_tag() for prim in combination[:layer]])

                    if layer <= combination_length - 1:
                        output_column_name += '.' + str(layer)
                        for output_dict in final_primitive.get_outputs():
                            out_name = output_dict['name']
                            final_primitive_outputs[numbered_primitive_name][out_name] = \
                                f'{output_column_name}.' + str(out_name)
                    else:
                        npn = numbered_primitive_name[:]  # lint
                        for output_dict in final_primitive.get_outputs():
                            out_name = output_dict['name']
                            final_outputs.append({'name': output_column_name + '.' + str(out_name),
                                                  'variable': f'{npn}.{out_name}'})
        return MLPipeline(
            primitives=final_primitives_list,
            init_params=final_init_params,
            input_names=final_primitive_inputs,
            output_names=final_primitive_outputs,
            outputs={'default': final_outputs}
        )

    def get_primitives(self):
        """Get a list of primitives in the pipeline."""
        return self.primitives.copy()

    def get_output_features(self):
        """Get a list of output feature tuples produced by the pipeline."""
        return [x[:] for x in self.primitive_combinations]


def build_tree_pipeline(transformation_layers, aggregation_layer):
    """
    Build a tree pipeline using given transformation and aggregation layers.

    Args:
        transformation_layers (list): List of transformation layers, each
        a list of transformation primitives.

        aggregation_layer (list): List of aggregation primitives

    Returns:
        sigpro.pipeline.LayerPipeline:
            A ``LayerPipeline`` object that produces the features in the Cartesian product
            of all transformation layers and the aggregation layer.
    """
    primitives_all = set()
    all_layers = []

    if not isinstance(transformation_layers, list):
        raise ValueError('transformation_layers must be a list')
    for layer in transformation_layers:
        if isinstance(layer, list):
            for primitive_ in layer:
                if not isinstance(primitive_, Primitive):
                    raise ValueError('Non-primitive specified in transformation_layers')
            all_layers.append(layer.copy())
            primitives_all.update(layer)
        else:
            raise ValueError('Each layer in transformation_layers must be a list')
    if isinstance(aggregation_layer, list):
        for primitive_ in aggregation_layer:
            if not isinstance(primitive_, Primitive):
                raise ValueError('Non-primitive specified in aggregation_layer')
        all_layers.append(aggregation_layer.copy())
        primitives_all.update(aggregation_layer)
    else:
        raise ValueError('aggregation_layer must be a list')

    primitive_combinations = list(product(*all_layers))
    return LayerPipeline(primitives=list(primitives_all),
                         primitive_combinations=primitive_combinations)


def build_layer_pipeline(primitives, primitive_combinations):
    """
    Layer pipeline building.

    Build a layer pipeline from a list of primitives and a list of
    combination features, each a tuple of Primitives.
    """
    return LayerPipeline(primitives=primitives,
                         primitive_combinations=primitive_combinations,
                         features_as_strings=False)


def build_layer_pipeline_str(primitives, primitive_combinations):
    """
    Layer pipeline building.

    Build a layer pipeline from a list of primitives and a list of
    combination features, each a tuple of string tags of primitives.
    """
    return LayerPipeline(primitives=primitives,
                         primitive_combinations=primitive_combinations,
                         features_as_strings=True)


def merge_pipelines(pipelines):
    """
    Create a single layer pipeline that is the 'union' of several other pipelines.

    In other words, the pipeline generates all features generated by
    at least one input pipeline.

    Args:
        pipelines (list): a list of Pipeline objects whose output features should be merged.

    Returns:
        sigpro.pipeline.LayerPipeline:
            A ``LayerPipeline`` object that produces the features in the union of
            all features generated by the input pipelines.

    """
    primitives_all = set()
    primitive_combinations = set()

    for pipeline in (pipelines)[::-1]:

        primitives_all.update(pipeline.get_primitives())
        primitive_combinations.update(pipeline.get_output_features())

    return LayerPipeline(primitives=list(primitives_all),
                         primitive_combinations=list(primitive_combinations))
