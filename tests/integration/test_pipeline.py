"""Test module for SigPro pipeline module."""

from sigpro import basic_primitives, pipeline, primitive


def test_linear_pipeline():
    """build_linear_pipeline test."""

    transformations = [basic_primitives.Identity(), basic_primitives.FFTReal()]
    aggregations = [basic_primitives.Mean(), basic_primitives.Kurtosis(fisher=True,bias=True)]

    assert isinstance(transformations[0], primitive.Primitive)

    sample_pipeline = pipeline.build_linear_pipeline(transformations, aggregations)  # incomplete

    assert isinstance(sample_pipeline, pipeline.LinearPipeline)


def test_tree_pipeline():
    """build_tree_pipeline test."""
    assert True


def test_layer_pipeline():
    """build_layer_pipeline test."""
    assert True
