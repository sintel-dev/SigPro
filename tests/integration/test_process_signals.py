# -*- coding: utf-8 -*-

import pandas as pd
from mlblocks import MLBlock
from pandas import Timestamp
from pandas.testing import assert_frame_equal

from sigpro.demo import get_demo_data
from sigpro.process_signals import process_signals


def test_process_signals():
    """Test the function ``process_signals``.

    Test that ``process_signals`` applies a list of primitives to the demo data and generates
    new features.

    Input:
        - data (pd.DataFrame): The demo data.
        - transformations (list): List of sigpro transformations to apply.
        - aggregations (list): List of sigpro aggregations to apply.
        - keep_values (bool): Return the values column or delete it.
        - values_column (str): Column name for the signals values.
        - kwargs: Additional args to work.

    Output:
        - The featurized dataframe.
    """
    # Setup
    data = get_demo_data(5)

    transformations = [
        {
            'name': 'fft',
            'primitive': 'sigpro.transformations.frequency.fft.fft_real',
        },
        {
            'name': 'band',
            'primitive': 'sigpro.transformations.frequency.band.frequency_band',
            'init_params': {
                'low': 100,
                'high': 1000
            }
        },
    ]

    aggregations = [
        {
            'name': 'rms',
            'primitive': 'sigpro.aggregations.amplitude.statistical.rms',
        },
        {
            'name': 'mean',
            'primitive': 'sigpro.aggregations.amplitude.statistical.mean',
        },
    ]

    # run
    result = process_signals(data, transformations, aggregations, sampling_frequency=10000)

    # assert
    expected_result = pd.DataFrame({
        'turbine_id': {
            0: 'T001',
            1: 'T001',
            2: 'T001',
            3: 'T001',
            4: 'T001'
        },
        'signal_id': {
            0: 'Sensor1_signal1',
            1: 'Sensor1_signal1',
            2: 'Sensor1_signal1',
            3: 'Sensor1_signal1',
            4: 'Sensor1_signal1'
        },
        'timestamp': {
            0: Timestamp('2020-01-01 00:00:00'),
            1: Timestamp('2020-01-01 01:00:00'),
            2: Timestamp('2020-01-01 02:00:00'),
            3: Timestamp('2020-01-01 03:00:00'),
            4: Timestamp('2020-01-01 04:00:00')
        },
        'fft.band.rms.rms_value': {
            0: 13.520619328031275,
            1: 12.814229400509381,
            2: 18.34211751830319,
            3: 11.989327742165269,
            4: 13.554189188523914
        },
        'fft.band.mean.mean_value': {
            0: 4.784187550373485,
            1: -2.6254568263243856,
            2: -3.14619864168385,
            3: -3.127326866240511,
            4: -1.0049470688766582
        },
    })

    assert_frame_equal(result, expected_result)


def test_process_signals_keep_values():
    """Test the function ``process_signals``.

    Test that ``process_signals`` applies a list of primitives to the demo data and generates
    new features.

    Input:
        - data (pd.DataFrame): The demo data.
        - transformations (list): List of sigpro transformations to apply.
        - aggregations (list): List of sigpro aggregations to apply.
        - keep_values (bool): Return the values column or delete it.
        - values_column (str): Column name for the signals values.
        - kwargs: Additional args to work.

    Output:
        - The featurized dataframe.
    """
    # Setup
    transformations = [
        {
            'name': 'identity',
            'primitive': 'sigpro.transformations.amplitude.identity.identity',
        }
    ]

    aggregations = [
        {
            'name': 'mean',
            'primitive': 'sigpro.aggregations.amplitude.statistical.mean',
        },
    ]

    data = pd.DataFrame({
        'timestamp': [
            Timestamp('2020-01-01 00:00:00'),
        ],
        'signal_values': [[1, 2, 3]],
    })

    # run
    result = process_signals(
        data,
        transformations,
        aggregations,
        values_column='signal_values',
        keep_values=True,
    )
    # assert
    expected_result = pd.DataFrame({
        'timestamp': [
            Timestamp('2020-01-01 00:00:00'),
        ],
        'signal_values': [[1, 2, 3]],
        'identity.mean.mean_value': [2.0],
    })

    assert_frame_equal(result, expected_result)


def test_process_signals_primitive():
    primitive = 'sigpro.process_signals.process_signals'
    transformations = [
        {
            'name': 'identity',
            'primitive': 'sigpro.transformations.amplitude.identity.identity',
        },

    ]
    aggregations = [
        {
            'name': 'mean',
            'primitive': 'sigpro.aggregations.amplitude.statistical.mean',
        },
    ]
    data = pd.DataFrame({
        'timestamp': [
            Timestamp('2020-01-01 00:00:00'),
        ],
        'signal_values': [[1, 2, 3]],
    })

    init_params = {
        'data': data,
        'transformations': transformations,
        'aggregations': aggregations,
        'values_column': 'signal_values'
    }

    primitive = MLBlock(primitive, **init_params)
    result = primitive.produce()
    expected_result = pd.DataFrame({
        'timestamp': [
            Timestamp('2020-01-01 00:00:00'),
        ],
        'identity.mean.mean_value': [2.0],
    })

    assert_frame_equal(result, expected_result)


def test_process_signals_sampling_frequency_str():
    """Test the function ``process_signals``.

    Test that ``process_signals`` applies a list of primitives to the demo data and generates
    new features.

    Input:
        - data (pd.DataFrame): The demo data.
        - transformations (list): List of sigpro transformations to apply.
        - aggregations (list): List of sigpro aggregations to apply.
        - sampling_frequency: Name of the column that contains the sampling frequency.
        - values_column (str): Column name for the signals values.
        - keep_values (bool): Return the values column or delete it.

    Output:
        - The featurized dataframe.
    """
    # Setup
    transformations = [
        {
            'name': 'fft',
            'primitive': 'sigpro.transformations.frequency.fft.fft_real',
        },
        {
            'name': 'band',
            'primitive': 'sigpro.transformations.frequency.band.frequency_band',
            'init_params': {
                'low': 9,
                'high': 21
            }
        },
    ]

    aggregations = [
        {
            'name': 'mean',
            'primitive': 'sigpro.aggregations.amplitude.statistical.mean',
        },
    ]

    data = pd.DataFrame({
        'timestamp': [
            Timestamp('2020-01-01 00:00:00'),
            Timestamp('2020-01-01 01:00:00'),
        ],
        'signal_values': [
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ],
        'sampling_frequency_values': [
            100,
            10
        ],
    })

    # run
    result = process_signals(
        data,
        transformations,
        aggregations,
        values_column='signal_values',
        sampling_frequency='sampling_frequency_values'
    )

    # assert

    expected_result = pd.DataFrame({
        'timestamp': [
            Timestamp('2020-01-01 00:00:00'),
            Timestamp('2020-01-01 01:00:00'),
        ],
        'sampling_frequency_values': [
            100,
            10
        ],
        'fft.band.mean.mean_value': [-5.0, float('nan')],
    })

    assert_frame_equal(result, expected_result)
