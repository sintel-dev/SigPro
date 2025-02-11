"""Test module for SigPro pipeline module."""
import pandas as pd
import pytest

from sigpro import pipeline, primitive
from sigpro.basic_primitives import FFT, BandMean, FFTReal, Identity, Kurtosis, Mean

TEST_INPUT = pd.DataFrame({'timestamp': pd.to_datetime(['2020-01-01 00:00:00']),
                           'values': [[1, 2, 3, 4, 5, 6]],
                           'sampling_frequency': [10000],
                           'dummy': [1], })

TEST_OUTPUT = pd.DataFrame({'fftr.id1.bm.value': [(-3 + 0j)],
                            'fftr.id1.mean.mean_value': [(1 + 0j)],
                            'fftr.mean.mean_value': [(1 + 0j)],
                            'fftr.id1.kurtosis.kurtosis_value': [(4.2 + 0j)],
                            'fftr.id2.bm.value': [(-3 + 0j)],
                            'fftr.id2.mean.mean_value': [(1 + 0j)],
                            'fftr.id2.kurtosis.kurtosis_value': [(4.2 + 0j)],
                            'fft.id1.bm.value': [(-3 + 3.4641016151377544j)],
                            'fft.id1.mean.mean_value': [(1 + 0j)],
                            'fft.id1.kurtosis.kurtosis_value': [(5.34 + 3.866899242231838e-18j)],
                            'fft.id2.bm.value': [(-3 + 3.4641016151377544j)],
                            'fft.id2.mean.mean_value': [(1 + 0j)],
                            'fft.id2.kurtosis.kurtosis_value': [(5.34 + 3.866899242231838e-18j)]})


def _verify_pipeline_outputs(sigpro_pipeline, input_data, output_data, columns_to_check=None):
    """Verify that a pipeline produces the output data on a set of dataframe inputs."""
    assert isinstance(sigpro_pipeline, pipeline.Pipeline)
    assert input_data is not None
    assert output_data is not None
    assert columns_to_check != []

    processed_signal, feature_list = sigpro_pipeline.process_signal(input_data)
    if columns_to_check is None:
        columns_to_check = feature_list[:]
    for column in columns_to_check:
        assert column in feature_list
        assert column in processed_signal.columns
    cols_reduced = [i for i in columns_to_check if i in output_data.columns]
    pd.testing.assert_frame_equal(processed_signal[cols_reduced], output_data[cols_reduced], rtol=1e-2)


def test_linear_pipeline():
    """build_linear_pipeline test."""

    transformations = [Identity().set_tag('id1'), FFTReal().set_tag('fftr')]
    aggregations = [Mean(), Kurtosis(fisher=False)]

    assert isinstance(transformations[0], primitive.Primitive)

    sample_pipeline = pipeline.build_linear_pipeline(transformations, aggregations)  # incomplete

    assert isinstance(sample_pipeline, pipeline.LinearPipeline)

    _verify_pipeline_outputs(sample_pipeline, TEST_INPUT, TEST_OUTPUT)


def test_tree_pipeline():
    """build_tree_pipeline test."""

    t_layer1 = [FFTReal().set_tag('fftr'), FFT()]
    t_layer2 = [Identity().set_tag('id1'), Identity().set_tag('id2')]

    a_layer = [BandMean(200, 50000).set_tag('bm'), Mean(), Kurtosis(fisher=False)]

    sample_pipeline = pipeline.build_tree_pipeline([t_layer1, t_layer2], a_layer)

    assert isinstance(sample_pipeline, pipeline.LayerPipeline)
    assert len(set(sample_pipeline.get_output_features())) == 12  # 2 * 2 * 3

    _verify_pipeline_outputs(sample_pipeline, TEST_INPUT, TEST_OUTPUT)


def test_layer_pipeline():
    """build_layer_pipeline test."""

    p1, p2 = FFTReal().set_tag('fftr'), FFT()
    p3, p4 = Identity().set_tag('id1'), Identity().set_tag('id2')
    p5, p6, p7 = BandMean(200, 50000).set_tag('bm'), Mean(), Kurtosis(fisher=False)
    p8 = Identity().set_tag('id3')  # unused primitive

    all_primitives = [p1, p2, p3, p4, p5, p6, p7, p8]

    features = [(p1, p3, p5), (p1, p3, p6), (p2, p3, p6), (p2, p4, p6), (p2, p4, p7), (p1, p6)]

    sample_pipeline = pipeline.build_layer_pipeline(all_primitives, features)

    assert isinstance(sample_pipeline, pipeline.LayerPipeline)

    out_features = sample_pipeline.get_output_combinations()
    for feature in features:
        assert feature in out_features

    _verify_pipeline_outputs(sample_pipeline, TEST_INPUT, TEST_OUTPUT)


def test_merge_pipelines():
    """merge_pipelines test."""
    p1, p2 = FFTReal().set_tag('fftr'), FFT()
    p3, p4 = Identity().set_tag('id1'), Identity().set_tag('id2')
    p5, p6, p7 = BandMean(200, 50000).set_tag('bm'), Mean(), Kurtosis(fisher=False)
    p8 = Identity().set_tag('id3')  # unused primitive

    all_primitives = [p1, p2, p3, p4, p5, p6, p7, p8]

    features1 = [(p1, p3, p5), (p1, p3, p6), (p2, p3, p6), (p2, p4, p6), (p2, p4, p7)]

    sample_pipeline1 = pipeline.build_layer_pipeline(all_primitives, features1)

    sample_pipeline2 = pipeline.build_tree_pipeline([[p1, p2], [p3]], [p5])

    sample_pipeline3 = pipeline.build_linear_pipeline([p1, p4], [p6])

    features = features1 + [(p2, p3, p5), (p1, p4, p6)]
    sample_pipeline = pipeline.merge_pipelines([sample_pipeline1,
                                                sample_pipeline2,
                                                sample_pipeline3])

    assert isinstance(sample_pipeline, pipeline.LayerPipeline)

    out_features = sample_pipeline.get_output_combinations()
    for feature in features:
        assert feature in out_features


def test_invalid_tree_pipelines():
    """Test invalid tree pipelines."""

    p1, p2, p2_duplicate = FFTReal().set_tag('fftr'), FFT(), FFT()
    p3, p4 = Identity().set_tag('id1'), Identity().set_tag('id2')
    p5, p6, p7 = BandMean(200, 50000).set_tag('bm'), Mean(), Kurtosis(fisher=False)

    t_layer1 = [p1, p2]
    t_layer2 = [p3, p4]

    a_layer = [p5, p6, p7]

    # Empty Cartesian product
    with pytest.raises(ValueError):
        pipeline.build_tree_pipeline([t_layer1, []], a_layer)
    with pytest.raises(ValueError):
        pipeline.build_tree_pipeline([[], t_layer2], a_layer)
    with pytest.raises(ValueError):
        pipeline.build_tree_pipeline([t_layer1, t_layer2], [])

    # Duplicate tags
    with pytest.raises(ValueError):
        pipeline.build_tree_pipeline([t_layer1 + [p2_duplicate], t_layer2], a_layer)

    # Incorrect primitive order
    with pytest.raises(ValueError):
        pipeline.build_tree_pipeline([t_layer1, a_layer], t_layer2)


def test_invalid_layer_pipelines():
    """Test invalid pipeline formation."""

    p1, p2, p2_duplicate = FFTReal().set_tag('fftr'), FFT(), FFT()
    p3, p4 = Identity().set_tag('id1'), Identity().set_tag('id2')
    p5, p6, p7 = BandMean(200, 50000).set_tag('bm'), Mean(), Kurtosis(fisher=False)
    p8 = Identity().set_tag('id3')  # unused primitive

    all_primitives = [p1, p2, p3, p4, p5, p6, p7, p8]

    all_primitives_duplicate = all_primitives + [p2_duplicate]

    features = [(p1, p3, p5), (p1, p3, p6), (p2, p3, p6), (p2, p4, p6), (p2, p4, p7)]

    no_agg_end = (p1, p3, p4)
    intermediate_agg = (p1, p6, p7)

    blank_features = [tuple(), tuple()]

    # Primitive in combination not contained in primitives
    with pytest.raises(ValueError):
        pipeline.build_layer_pipeline([p1, p2, p3, p5, p6, p7, p8], features)

    # Duplicate primitive
    with pytest.raises(ValueError):
        pipeline.build_layer_pipeline(all_primitives_duplicate, features)

    # No nontrivial features
    with pytest.raises(ValueError):
        pipeline.build_layer_pipeline([p1, p3, p5], blank_features)

    with pytest.raises(ValueError):
        pipeline.build_layer_pipeline([p1, p3, p5], [])

    # At least one feature in incorrect format
    with pytest.raises(ValueError):
        pipeline.build_layer_pipeline(all_primitives, features + [no_agg_end])

    with pytest.raises(ValueError):
        pipeline.build_layer_pipeline(all_primitives, features + [intermediate_agg])
