import pandas as pd
from mlblocks import MLPipeline


def test_process_signals():
    pipeline = MLPipeline({
        'primitives': [
            'sigpro.process_signals',
            'sigpro.process_signals',
        ],
        'init_params': {
            'sigpro.process_signals#1': {
                'values_column_name': 'signal_values',
                'keep_columns': True,
                'transformations': [
                    {
                        'name': 'identity',
                        'primitive': 'sigpro.transformations.amplitude.identity.identity',
                    },
                    {
                        'name': 'fft',
                        'primitive': 'sigpro.transformations.frequency.fft.fft_real',
                    },
                ],
                'aggregations': [
                    {
                        'name': 'mean',
                        'primitive': 'sigpro.aggregations.amplitude.statistical.mean',
                    },
                    {
                        'name': 'rms',
                        'primitive': 'sigpro.aggregations.amplitude.statistical.rms',
                    },
                ]
            },
            'sigpro.process_signals#2': {
                'values_column_name': 'signal_values',
                'keep_columns': ['dummy'],
                'transformations': [
                    {
                        'name': 'identity',
                        'primitive': 'sigpro.transformations.amplitude.identity.identity',
                    },
                ],
                'aggregations': [
                    {
                        'name': 'std',
                        'primitive': 'sigpro.aggregations.amplitude.statistical.std',
                    },
                ]
            }
        }
    })

    data = pd.DataFrame({
        'timestamp': pd.to_datetime(['2020-01-01 00:00:00']),
        'signal_values': [[1, 2, 3, 4]],
        'sampling_frequency': [1000],
        'dummy': [1],
    })

    output = pipeline.predict(readings=data)
    outputs = dict(zip(pipeline.get_output_names(), output))

    expected_features = [
        'identity.fft.mean.mean_value',
        'identity.fft.rms.rms_value',
        'identity.std.std_value'
    ]
    assert outputs['feature_columns'] == expected_features

    expected_readings = pd.DataFrame({
        'dummy': [1],
        'identity.fft.mean.mean_value': [1.0],
        'identity.fft.rms.rms_value': [5.291503],
        'identity.std.std_value': [1.118034],
    })
    pd.testing.assert_frame_equal(expected_readings, outputs['readings'])
