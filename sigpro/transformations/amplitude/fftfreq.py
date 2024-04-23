"""Build power spectrum from amplitude values."""


import numpy as np


def fft_freq(amplitude_values, sampling_frequency):
    """Compute the Frequency having FFT values

    Args:
        amplitude_values (np.ndarray):
            A numpy array with the signal values.
        sampling_frequency (int or float):
            Sampling frequency value passed in Hz.
    Returns:
        tuple:
            * `amplitude_values (numpy.ndarray)`
            * `frequency_values (numpy.ndarray)`
    """
    amplitude_values = amplitude_values
    frequency_values = np.fft.fftfreq(len(amplitude_values), 1 / sampling_frequency)

    return amplitude_values, frequency_values