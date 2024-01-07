# -*- coding: utf-8 -*-
"""Process Signals core functionality."""

from collections import Counter
from copy import deepcopy
from itertools import product
from abc import ABC

import pandas as pd
from mlblocks import MLPipeline, load_primitive
from mlblocks.mlblock import import_object


from sigpro import contributing, primitive
from sigpro.primitive import Primitive
from sigpro.basic_primitives import Identity
import json
import inspect


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

    def __init__(self):
        self.values_column_name = 'values'
        self.input_is_dataframe = True
        self.pipeline = None

    def get_pipeline(self):
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
        raise NotImplementedError 

    def get_output_features(self):
        raise NotImplementedError

    def process_signal(self, data=None, window=None, values_column_name = 'values', time_index=None, groupby_index=None, 
                       feature_columns=None,  keep_columns = False, input_is_dataframe = True,  **kwargs):
        """Apply multiple transformation and aggregation primitives.

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
                    ``keep_values`` is ``True`` the original signal values will be conserved in the
                    data frame, otherwise the original signal values will be deleted.
                list:
                    A list with the feature names generated.
        """
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

    
"""
Analogue of sigpro.SigPro object in current use, takes in same arguments.
Only distinction is that we accept primitive objects, rather than dict inputs.
"""
class LinearPipeline(Pipeline): 

    def __init__(self, transformations, aggregations): 

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

            # primitive_outputs = getattr(self, primitive_outputs)()
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
        return self.transformations.copy() + self.aggregations.copy()
        
    def get_output_features(self):
        return [ tuple(self.transformations.copy() + [aggregation]) for aggregation in self.aggregations]

def build_linear_pipeline(transformations, aggregations):
    pipeline_object = LinearPipeline(transformations, aggregations)
    return pipeline_object


def _tag_tuples_to_objects(primitives, tag_tuples):
    """
    Given a list of primitive objects, convert a list of tuples of primitive tags given in tag_tuples to a list of primitive objects.
    """
    tags = [p.get_tag() for p in primitives]
    if len(tags) > len(set(tags)):
        raise ValueError('Not all primitives have distinct tags')
    primitives_dict = {primitive.get_tag(): primitive for primitive in primitives}
    return [tuple(primitives_dict[tag] for tag in tag_tuple) for tag_tuple in tag_tuples]
    

class LayerPipeline(Pipeline):

    def __init__(self, primitives, primitive_combinations, features_as_strings = False):
        """
        Initialize a LayerPipeline.
        
        Args:
            primitives (list): List of primitive objects
                
            primitive_combinations (list): List of output features to be generated. Each combination in primitive_combinations should be a tuple (or list) of primitive objects 
                found as keys in primitives, or a tuple (or list) of their string tags.
                All lists should  end with a single aggregation primitive. 

            features_as_strings (bool): True if primitive_combinations is defined with string names, False if primitive_combinations is defined with primitive objects (default).

        Returns:
            LayerPipeline that generates the primitives in primitive_combinations.
        """
        super().__init__()
        if isinstance(primitives, list):
            primitives_dict = {}
            for primitive in primitives:
                if not(isinstance(primitive, Primitive)):
                    raise ValueError('Non-primitive specified in list primitives')

                if primitive.get_tag() in primitives_dict:
                    raise ValueError(f'Tag {primitive.get_tag()} duplicated in list primitives. All primitives must have distinct tags.')

                primitives_dict[primitive.get_tag()] = primitive
            self.primitives = primitives.copy() #_dict
        else:
            raise ValueError('primitives must a list')

        self.primitive_combinations = None
        if len(primitive_combinations) == 0:
            raise ValueError('At least one feature must be specified')
        else:
            if features_as_strings:
                primitive_combinations = [tuple(primitives_dict[tag] for tag in tag_tuple) for tag_tuple in primitive_combinations]

            self.primitive_combinations = [tuple(combination) for combination in primitive_combinations]

        length = max([len(combination) for combination in primitive_combinations] + [0])

        if length == 0:
            raise ValueError('At least one non-empty output feature must be specified')
        self.num_layers = length

        for combination in self.primitive_combinations:

            l = len(combination)
            for i in range(l-1):
                if combination[i].get_type_subtype()[0] != 'transformation':
                    raise ValueError(f'Primitive at non-terminal position #{i+1}/{l} is not a transformation')
            
            if combination[-1].get_type_subtype()[0] != 'aggregation':
                raise ValueError(f'Last primitive is not an aggregation')

            for primitive in combination:
                if primitive not in self.primitives:
                    raise ValueError(f'Primitive with tag {primitive.get_tag()} not found in the given primitives')

        self.pipeline = self._build_pipeline()
    
    def _build_pipeline(self):
        """
        Segment of code that actually builds the pipeline.
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

                    if layer == combination_length:
                        assert (tuple(combination[:layer]) not in prefixes) #Since all combinations are T.T.T...T.A, the full combination of one combination should never be a prefix.

                    final_primitive = combination[layer - 1] 
                    final_primitive_str = final_primitive.get_tag()

                    prefixes[(tuple(combination[:layer]))] =  final_primitive

                    final_primitive_name = final_primitive.get_name()
                    final_primitives_list.append(final_primitive.get_name()) 
                    primitive_counter[final_primitive_name] += 1
                    numbered_primitive_name = f'{final_primitive_name}#{primitive_counter[final_primitive_name]}'

                    final_init_params[numbered_primitive_name] = final_primitive.get_hyperparam_dict()['init_params']

                    final_primitive_inputs[numbered_primitive_name] = {}
                    final_primitive_outputs[numbered_primitive_name] = {}

                    for input_dict in final_primitive.get_inputs():
                        final_primitive_inputs[numbered_primitive_name][input_dict['name']] = f'{final_primitive_str}.' + str(input_dict['name'])
                    if layer == 1:
                        final_primitive_inputs[numbered_primitive_name]['amplitude_values'] = 'amplitude_values'
                    else:
                        input_column_name = '.'.join([prim.get_tag() for prim in combination[:layer - 1]]) + f'.{layer-1}' 
                        final_primitive_inputs[numbered_primitive_name]['amplitude_values'] = input_column_name + '.amplitude_values'

                    output_column_name = '.'.join([prim.get_tag() for prim in combination[:layer]])

                    if layer <= combination_length - 1: 
                        output_column_name +=   '.' + str(layer)
                        for output_dict in final_primitive.get_outputs(): 
                            final_primitive_outputs[numbered_primitive_name][output_dict['name']] = f'{output_column_name}.' + str(output_dict['name'])
                    else:
                       for output_dict in final_primitive.get_outputs():
                        out_name = output_dict['name']
                        final_outputs.append({'name':   output_column_name + '.' + str(out_name), 'variable': f'{numbered_primitive_name}.{out_name}' })


        return MLPipeline( 
            primitives = final_primitives_list,
            init_params = final_init_params,
            input_names = final_primitive_inputs,
            output_names = final_primitive_outputs,
            outputs = {'default': final_outputs}
        )
    def get_primitives(self):
        return self.primitives.copy()

    def get_output_features(self):
        return [x[:] for x in self.primitive_combinations]

def build_tree_pipeline(transformation_layers, aggregation_layer):

    primitives_all = set()
    all_layers = []

    if not(isinstance(transformation_layers, list)):
        raise ValueError('transformation_layers must be a list')
    for layer in transformation_layers:
        if isinstance(layer, list):
            for primitive in layer:
                if not(isinstance(primitive, Primitive)):
                    raise ValueError('Non-primitive specified in transformation_layers')
            all_layers.append(layer.copy())
            primitives_all.update(layer)
        else:
            raise ValueError('Each layer in transformation_layers must be a list')
    
    if isinstance(aggregation_layer, list):
        for primitive in aggregation_layer:
            if not(isinstance(primitive, Primitive)):
                raise ValueError('Non-primitive specified in aggregation_layer')
        all_layers.append(aggregation_layer.copy())
        primitives_all.update(aggregation_layer)
    
    else:
        raise ValueError('aggregation_layer must be a list')


    primitive_combinations = list(product(*all_layers))
    return LayerPipeline(primitives = list(primitives_all), primitive_combinations = primitive_combinations)


def build_layer_pipeline(primitives, primitive_combinations):
    return LayerPipeline(primitives = primitives, primitive_combinations = primitive_combinations, features_as_strings = False)

def build_layer_pipeline_str(primitives, primitive_combinations):
    return LayerPipeline(primitives = primitives, primitive_combinations = primitive_combinations, features_as_strings = True)


def merge_pipelines(pipelines):

    """
    Create a single layer pipeline that is the 'union' of several other pipelines; that is, the pipeline generates all features generated by at least one input pipeline.

    Pipeline merges are done by merging the feature tuples of the primitive names, which are user-assigned strings or primitive tags. 
    If two primitives in distinct pipelines are given the same label, the default behavior is to pick the primitive object in the earliest pipeline with that particular label,
    and override all later objects.
    Args:
        pipelines (list): a list of Pipeline objects whose output features should be merged.

    """
    primitives_all = set()
    primitive_combinations = set()

    for pipeline in (pipelines)[::-1]: 

        primitives_all.update(pipeline.get_primitives())
        primitive_combinations.update(pipeline.get_output_features())


    return LayerPipeline(primitives = list(primitives_all), primitive_combinations = list(primitive_combinations))
