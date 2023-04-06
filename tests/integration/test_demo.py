"""Test module for SigPro demo."""
import numpy as np

from sigpro.demo import (
    get_amplitude_demo, get_demo_data, get_demo_primitives, get_frequency_demo,
    get_frequency_time_demo)

EXPECTED_SHAPE = (300000, 5)
EXPECTED_COLUMNS = ['turbine_id', 'signal_id', 'timestamp', 'values', 'sampling_frequency']
EXPECTED_SAMPLING_FREQUENCY = 10000
EXPECTED_VALUES_LENGTH = 400
EXPECTED_FREQUENCY_LENGTH = 400


def test_get_demo_data():
    df = get_demo_data()
    assert EXPECTED_SHAPE == df.shape
    assert EXPECTED_COLUMNS == list(df.columns)


def test_get_demo_primitives():
    trans, aggs = get_demo_primitives()
    assert len(trans) == 1
    assert len(aggs) == 2
    for primitive in [*trans, *aggs]:
        assert 'name' in primitive
        assert 'primitive' in primitive


def test_get_amplitude_demo_without_index():
    values, sampling_frequency = get_amplitude_demo()
    assert EXPECTED_VALUES_LENGTH == len(values)
    assert EXPECTED_SAMPLING_FREQUENCY == sampling_frequency


def test_get_amplitude_demo_indexed():
    values, sampling_frequency = get_amplitude_demo(index=1)
    assert EXPECTED_VALUES_LENGTH == len(values)
    assert EXPECTED_SAMPLING_FREQUENCY == sampling_frequency


def test_get_frequency_demo_without_index():
    values, frequency_values = get_frequency_demo()
    assert EXPECTED_VALUES_LENGTH // 2 == len(values)
    assert EXPECTED_FREQUENCY_LENGTH // 2 == len(frequency_values)


def test_get_frequency_demo_indexed():
    values, frequency_values = get_frequency_demo(index=1)
    assert EXPECTED_VALUES_LENGTH // 2 == len(values)
    assert EXPECTED_FREQUENCY_LENGTH // 2 == len(frequency_values)


def test_get_frequency_demo_complex():
    values, frequency_values = get_frequency_demo(real=False)
    value = values[0]
    assert isinstance(value, np.complex128)
    assert EXPECTED_VALUES_LENGTH // 2 == len(values)
    assert EXPECTED_FREQUENCY_LENGTH // 2 == len(frequency_values)


def test_get_frequency_time_demo_without_index():
    values, frequencies, time_values = get_frequency_time_demo()
    assert 129 == len(values)
    assert 129 == len(frequencies)
    assert 5 == len(time_values)


def test_get_frequency_time_demo_indexed():
    values, frequencies, time_values = get_frequency_time_demo(index=1)
    assert 129 == len(values)
    assert 129 == len(frequencies)
    assert 5 == len(time_values)


def test_get_frequency_time_demo_complex():
    values, frequencies, time_values = get_frequency_time_demo(real=False)
    value = values[0][0]
    assert 129 == len(values)
    assert 129 == len(frequencies)
    assert 5 == len(time_values)
    assert isinstance(value, np.complex128)
