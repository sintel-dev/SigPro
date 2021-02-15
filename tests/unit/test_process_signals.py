"""Unit tests for the sigpro.process_signals module."""

import pandas as pd

from sigpro.process_signals import process_signals


def test_process_signals_keep_columns_false():
    """Test process_signals with keep_columns False.

    If keep_columns is false only the generated features are
    returned.

    Input:
        - data, transformations, aggregations
        - keep_columns=False

    Output:
        - pandas.DataFrame with the specified aggregations and nothing else.
        - feature_names that match the columns in the data frame.
    """

    data = pd.DataFrame({
        'values': [[1, 2, 3], [4, 5, 6]],
        'dummy': [1, 2],
    })

    output, feature_columns = process_signals(
        data,
        transformations=[
            {
                'name': 'identity',
                'primitive': 'sigpro.transformations.amplitude.identity.identity'
            }
        ],
        aggregations=[
            {
                'name': 'mean',
                'primitive': 'sigpro.aggregations.amplitude.statistical.mean',
            }
        ],
        keep_columns=False
    )

    expected = pd.DataFrame({
        'identity.mean.mean_value': [2.0, 5.0]
    })
    pd.testing.assert_frame_equal(expected, output)

    assert feature_columns == ['identity.mean.mean_value']


def test_process_signals_keep_columns_true():
    """Test process_signals with keep_columns True.

    If keep_columns is true the input columns are kept in the output
    dataframe

    Input:
        - data, transformations, aggregations
        - keep_columns=True

    Output:
        - pandas.DataFrame with the specified aggregations + the input columns
        - feature_names that match the new columns in the data frame.
    """

    data = pd.DataFrame({
        'values': [[1, 2, 3], [4, 5, 6]],
        'dummy': [1, 2],
    })

    output, feature_columns = process_signals(
        data,
        transformations=[
            {
                'name': 'identity',
                'primitive': 'sigpro.transformations.amplitude.identity.identity'
            }
        ],
        aggregations=[
            {
                'name': 'mean',
                'primitive': 'sigpro.aggregations.amplitude.statistical.mean',
            }
        ],
        keep_columns=True
    )

    expected = pd.DataFrame({
        'values': [[1, 2, 3], [4, 5, 6]],
        'dummy': [1, 2],
        'identity.mean.mean_value': [2.0, 5.0]
    })
    pd.testing.assert_frame_equal(expected, output)

    assert feature_columns == ['identity.mean.mean_value']


def test_process_signals_keep_columns_list():
    """Test process_signals with keep_columns passed as a list.

    If keep_columns is a list keep the indicated columns in the output
    dataframe and drop the rest.

    Input:
        - data (with a 'dummy' column), transformations, aggregations
        - keep_columns=['dummy']

    Output:
        - pandas.DataFrame with the specified aggregations + the 'dummy' column.
        - feature_names that match the new columns in the data frame.
    """

    data = pd.DataFrame({
        'values': [[1, 2, 3], [4, 5, 6]],
        'dummy': [1, 2],
    })

    output, feature_columns = process_signals(
        data,
        transformations=[
            {
                'name': 'identity',
                'primitive': 'sigpro.transformations.amplitude.identity.identity'
            }
        ],
        aggregations=[
            {
                'name': 'mean',
                'primitive': 'sigpro.aggregations.amplitude.statistical.mean',
            }
        ],
        keep_columns=['dummy'],
    )

    expected = pd.DataFrame({
        'dummy': [1, 2],
        'identity.mean.mean_value': [2.0, 5.0]
    })
    pd.testing.assert_frame_equal(expected, output)

    assert feature_columns == ['identity.mean.mean_value']


def test_process_signals_feature_columns_input():
    """Test process_signals with feature_columns as input.

    If feature_columns list is passed those columns are considered
    feature columns in the outpu.

    Input:
        - data (with a 'dummy' column), transformations, aggregations
        - feature_columns='dummy'

    Output:
        - pandas.DataFrame with the specified aggregations and the 'dummy' column.
        - feature_names that match the columns in the data frame + 'dummy'.
    """

    data = pd.DataFrame({
        'values': [[1, 2, 3], [4, 5, 6]],
        'dummy': [1, 2],
    })

    output, feature_columns = process_signals(
        data,
        transformations=[
            {
                'name': 'identity',
                'primitive': 'sigpro.transformations.amplitude.identity.identity'
            }
        ],
        aggregations=[
            {
                'name': 'mean',
                'primitive': 'sigpro.aggregations.amplitude.statistical.mean',
            }
        ],
        feature_columns=['dummy']
    )

    expected = pd.DataFrame({
        'dummy': [1, 2],
        'identity.mean.mean_value': [2.0, 5.0]
    })
    pd.testing.assert_frame_equal(expected, output)

    assert feature_columns == ['dummy', 'identity.mean.mean_value']
