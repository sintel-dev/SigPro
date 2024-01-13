"""Test module for SigPro pipeline module."""

from sigpro import pipeline, primitive
from sigpro.basic_primitives import FFT, BandMean, FFTReal, Identity, Kurtosis, Mean

# TODO: prepare a pair of INPUT, OUTPUT dataframes to check.


def _verify_pipeline_outputs(sigpro_pipeline, input_data, output_data, columns_to_check=None):
    """Verify that a pipeline produces the output data on a set of dataframe inputs."""
    assert isinstance(sigpro_pipeline, pipeline.Pipeline)
    assert input_data is not None
    assert output_data is not None
    assert columns_to_check != []


def test_linear_pipeline():
    """build_linear_pipeline test."""

    transformations = [Identity(), FFTReal()]
    aggregations = [Mean(), Kurtosis(fisher=True, bias=True)]

    assert isinstance(transformations[0], primitive.Primitive)

    sample_pipeline = pipeline.build_linear_pipeline(transformations, aggregations)  # incomplete

    assert isinstance(sample_pipeline, pipeline.LinearPipeline)

    # TODO: sanity-check feature output values.


def test_tree_pipeline():
    """build_tree_pipeline test."""

    t_layer1 = [Identity().set_tag('id1'), Identity().set_tag('id2')]
    t_layer2 = [FFTReal(), FFT()]
    a_layer = [BandMean(200, 500), Mean(), Kurtosis(fisher=False)]

    sample_pipeline = pipeline.build_tree_pipeline([t_layer1, t_layer2], a_layer)

    assert isinstance(sample_pipeline, pipeline.LayerPipeline)
    assert len(set(sample_pipeline.get_output_features())) == 12  # 2 * 2 * 3

    # TODO: sanity-check feature output values.


def test_layer_pipeline():
    """build_layer_pipeline test."""

    p1, p2 = Identity().set_tag('id1'), Identity().set_tag('id2')
    p3, p4 = FFTReal().set_tag('fftr'), FFT()
    p5, p6, p7 = BandMean(200, 500).set_tag('bm'), Mean(), Kurtosis(fisher=False)
    p8 = Identity().set_tag('id3')  # unused primitive

    all_primitives = [p1, p2, p3, p4, p5, p6, p7, p8]

    features = [(p1, p3, p5), (p1, p3, p6), (p2, p3, p6), (p2, p4, p6), (p1, p2, p7)]

    sample_pipeline = pipeline.build_layer_pipeline(all_primitives, features)

    assert isinstance(sample_pipeline, pipeline.LayerPipeline)

    out_features = sample_pipeline.get_output_features()
    for feature in features:
        assert feature in out_features

    # TODO: sanity-check feature output values.


def test_merge_pipelines():
    """marge_pipelines test."""
    p1, p2 = Identity().set_tag('id1'), Identity().set_tag('id2')
    p3, p4 = FFTReal().set_tag('fftr'), FFT()
    p5, p6, p7 = BandMean(200, 500).set_tag('bm'), Mean(), Kurtosis(fisher=False)
    p8 = Identity().set_tag('id3')  # unused primitive

    all_primitives = [p1, p2, p3, p4, p5, p6, p7, p8]

    features1 = [(p1, p3, p5), (p1, p3, p6), (p2, p3, p6), (p2, p4, p6), (p1, p2, p7)]

    sample_pipeline1 = pipeline.build_layer_pipeline(all_primitives, features1)

    sample_pipeline2 = pipeline.build_tree_pipeline([[p1, p2], [p3]], [p5])

    sample_pipeline3 = pipeline.build_linear_pipeline([p1, p4], [p6])

    features = features1 + [(p2, p3, p5), (p1, p4, p6)]
    sample_pipeline = pipeline.merge_pipelines([sample_pipeline1,
                                                sample_pipeline2,
                                                sample_pipeline3])

    assert isinstance(sample_pipeline, pipeline.LayerPipeline)

    out_features = sample_pipeline.get_output_features()
    for feature in features:
        assert feature in out_features

    # TODO: sanity-check feature output values.
