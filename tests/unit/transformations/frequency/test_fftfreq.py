"""Tests for sigpro.transformations.frequency module."""
import numpy as np
from sigpro.transformations.frequency import fft_freq_allband



def test_fft_freq_allband():
    # setup
    amplitude_values = [1.5, -0.5, 2.0, 0.5, -1.0]
    sampling_frequency = 2  # in Hz

    # run
    amplitude_result, frequency_result = fft_freq_allband(amplitude_values, sampling_frequency)

    # assert
    expected_amplitude_values = np.array([1.5, -0.5, 2.0, 0.5, -1.0])
    expected_frequency_values = np.array([0., 2., 4., 6., 8.])
    np.testing.assert_array_almost_equal(amplitude_result, expected_amplitude_values)
    np.testing.assert_array_almost_equal(frequency_result, expected_frequency_values)
