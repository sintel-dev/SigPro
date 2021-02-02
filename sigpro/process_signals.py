# -*- coding: utf-8 -*-
"""Process Signals core functionality."""

from collections import Counter

import pandas as pd
from mlblocks import MLPipeline, load_primitive


def _build_pipeline(transformations, aggregations):
    """Build Pipeline function.

    Given a list of transformations and aggregations build a pipeline
    with the output of the aggregations, which take as name the specified
    name of the transformations and the aggregation. This lists are composed
    by dictionaries with the following specification:

        * ``Name``:
            Name of the transformation / aggregation.
        * ``primitive``:
            Name of the primitive to apply.
        * ``init_params``:
            Dictionary containing the initializing parameters for the primitive.

    Args:
        transformations (list):
            List of dictionaries containing the transformation primitives.
        transformations (list):
            List of dictionaries containing the aggregation primitives.

    Returns:
        mlblocks.MLPipeline:
            An ``MLPipeline`` object that first applies all the transformations
            and then produces as output the aggregations specified.
    """
    primitives = []
    init_params = {}
    prefix = []
    outputs = []
    counter = Counter()

    for transformation in transformations:
        prefix.append(transformation['name'])
        primitive = transformation['primitive']
        counter[primitive] += 1
        primitive_name = f'{primitive}#{counter[primitive]}'
        primitives.append(primitive)
        params = transformation.get('init_params')
        if params:
            init_params[primitive_name] = params

    prefix = '.'.join(prefix) if prefix else ''

    for aggregation in aggregations:
        aggregation_name = f'{prefix}.{aggregation["name"]}' if prefix else aggregation['name']

        primitive = aggregation['primitive']
        counter[primitive] += 1
        primitive_name = f'{primitive}#{counter[primitive]}'
        primitives.append(primitive)

        primitive = load_primitive(primitive)
        primitive_outputs = primitive['produce']['output']

        for output in primitive_outputs:
            output = output['name']
            outputs.append({
                'name': f'{aggregation_name}.{output}',
                'variable': f'{primitive_name}.{output}'
            })

        params = aggregation.get('init_params')
        if params:
            init_params[primitive_name] = params

    outputs = {'default': outputs} if outputs else None

    return MLPipeline(
        primitives,
        init_params=init_params,
        outputs=outputs
    )


def _apply_pipeline(row, pipeline, values_column_name):
    """Apply a ``mlblocks.MLPipeline`` to a row.

    Apply a ``MLPipeline`` to a row of a ``pd.DataFrame``, this function can
    be combined with the ``pd.DataFrame.apply`` method to be applied to the
    entire data frame.

    Args:
        row (pd.Series):
            Row used to apply the pipeline to.
        pipeline (mlblocks.MLPipeline):
            Pipeline to be used for producing the results.
        values_column_name (str):
            The name of the column that contains the signal values.
    """
    context = row.to_dict()
    amplitude_values = context.pop(values_column_name)
    output = pipeline.predict(
        amplitude_values=amplitude_values,
        **context,
    )
    output_names = pipeline.get_output_names()

    # ensure that we can iterate over output
    output = output if isinstance(output, tuple) else (output, )

    return pd.Series(dict(zip(output_names, output)))


def process_signals(data, transformations, aggregations,
                    values_column_name='values', keep_values=False):
    """Process Signals.

    The Process Signals is responsible for applying a collection of primitives specified by the
    user in order to create features for the given data.

    Given a list of transformations and aggregations which are composed
    by dictionaries with the following specification:

        * ``Name``:
            Name of the transformation / aggregation.
        * ``primitive``:
            Name of the primitive to apply.
        * ``init_params``:
            Dictionary containing the initializing parameters for the primitive.

    The process signals will build an ``mlblocks.MLPipeline`` and will generate the features
    by previously applying the transformations and then compute the aggregations.

    Args:
        data (pandas.DataFrame):
            Dataframe with a column that contains signal values.
        transformations (list):
            List of dictionaries containing the transformation primitives.
        aggregations (list):
            List of dictionaries containing the aggregation primitives.
        values_column_name (str):
            The name of the column that contains the signal values. Defaults to ``values``.
        keep_values (bool):
            Whether or not to keep the original signal values or remove them.

    Returns:
        pandas.DataFrame:
            A data frame with new feature columns by applying the previous primitives. If
            ``keep_values`` is ``True`` the original signal values will be conserved in the
            data frame, otherwise the original signal values will be deleted.
    """
    pipeline = _build_pipeline(transformations, aggregations)
    features = data.apply(
        _apply_pipeline,
        args=(pipeline, values_column_name),
        axis=1
    )

    data = pd.concat([data, features], axis=1)

    if not keep_values:
        del data[values_column_name]

    return data
