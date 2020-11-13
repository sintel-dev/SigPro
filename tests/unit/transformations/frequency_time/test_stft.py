"""Tests for sigpro.transformations.frequency_time.stft module."""

import numpy as np

from sigpro.transformations.frequency_time.stft import stft, stft_real


def test_stft():
    # setup
    values = list(range(256))
    frequency = 10

    # run
    amplitude_values, frequency_values, time_values = stft(values, frequency)

    # assert
    expected_amplitude_values_len = 129
    expected_frequency_values_len = 129
    expected_time_values_len = 3
    value = amplitude_values[0][0]

    assert type(value) == np.complex128
    assert len(amplitude_values) == expected_amplitude_values_len
    assert len(frequency_values) == expected_frequency_values_len
    assert len(time_values) == expected_time_values_len


def test_stft_real():
    # setup
    values = list(range(256))
    frequency = 10

    # run
    amplitude_values, frequency_values, time_values = stft_real(values, frequency)

    # assert
    expected_amplitude_values_len = 129
    expected_frequency_values_len = 129
    expected_time_values_len = 3
    value = amplitude_values[0][0]

    assert type(value) == np.float64
    assert len(amplitude_values) == expected_amplitude_values_len
    assert len(frequency_values) == expected_frequency_values_len
    assert len(time_values) == expected_time_values_len
