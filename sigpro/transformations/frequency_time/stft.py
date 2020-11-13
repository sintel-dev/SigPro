"""Transformations Frequency Time - Short Time Fourier Transform module."""

import scipy.signal


def stft(amplitude_values, sampling_frequency):
    """Compute the Short Time Fourier Transform.

    Args:
        amplitude_values (np.ndarray):
            A numpy array with the signal values.
        sampling_frequency (int or float):
            Sampling frequency value passed in Hz.
    Returns:
        tuple:
            * `amplitude_values (numpy.ndarray)`
            * `frequency_values (numpy.ndarray)`
            * `time_values (numpy.ndarray)`
    """
    frequency_values, time_values, amplitude_values = scipy.signal.stft(
        amplitude_values,
        fs=sampling_frequency
    )
    return amplitude_values, frequency_values, time_values
