"""Band Module."""

import numpy as np


def band_mean(amplitude_values, frequency_values, min_frequency, max_frequency):
    """Compute the mean values for a specific band.
    Filter between a high and low band and compute the mean value for this specific band.

    Args:
        amplitude_values (np.ndarray):
            A numpy array with the signal values.
        frequency_values (np.ndarray):
            A numpy array with the frequency values.
        min_frequency (int or float):
            Band minimum.
        max_frequency (int or float):
            Band maximum.

    Returns:
        float:
            Mean value for the given band.
    """

    lower_frequency_than = frequency_values <= max_frequency
    higher_frequency_than = frequency_values >= min_frequency
    selected_idx = np.where(higher_frequency_than & lower_frequency_than)
    selected_values = amplitude_values[selected_idx]

    return np.mean(selected_values)


def band_rms(amplitude_values, frequency_values, min_frequency, max_frequency):
    """Compute the rms values for a specific band.
    Filter between a high and low band (inclusive) and compute the rms value for this
    specific band.

    Args:
        amplitude_values (np.ndarray):
            A numpy array with the signal values.
        frequency_values (np.ndarray):
            A numpy array with the frequency values.
        min_frequency (int or float):
            Band minimum.
        max_frequency (int or float):
            Band maximum.

    Returns:
        float:
            rms value for the given band.
    """

    lower_frequency_than = frequency_values <= max_frequency
    higher_frequency_than = frequency_values >= min_frequency

    selected_idx = np.ravel(np.where(np.ravel(higher_frequency_than & lower_frequency_than)))

    selected_idx = [int(x) for x in selected_idx]

    selected_values = np.array(amplitude_values)[selected_idx]

    return np.sqrt(np.mean(np.square(selected_values)))
