"""Test module for SigPro contributing module."""
from sigpro.contributing import run_primitive


def test_run_primitive_aggregation_no_hyperparameters():
    result = run_primitive('sigpro.aggregations.amplitude.statistical.mean', demo_row_index=0)
    assert round(result, 6) == 0.021361


def test_run_primitive_aggregation_hyperparameters():
    result_false = run_primitive(
        'sigpro.aggregations.amplitude.statistical.kurtosis',
        demo_row_index=0,
        fisher=False
    )

    result_default = run_primitive(
        'sigpro.aggregations.amplitude.statistical.kurtosis',
        demo_row_index=0,
    )

    assert result_false != result_default
    assert round(result_false, 6) == 2.280983
    assert round(result_default, 6) == -0.719017


def test_run_primitive_transformation():
    result = run_primitive('sigpro.transformations.frequency.fft.fft')
    assert len(result[0]) == 400
    assert len(result[1]) == 400
