"""SigPro Frequency Band module."""


def frequency_band(amplitude_values, frequency_values, low, high):
    """Extract a specific band.

    Filter between a high and low band frequency and return the amplitude values and frequency
    values for those.

    Args:
        amplitude_values (np.ndarray):
            A numpy array with the signal values.
        frequency_values (np.ndarray):
            A numpy array with the frequency values.
    Returns:
        tuple:
            * `amplitude_values (numpy.ndarray)` for the selected frequency values.
            * `frequency_values (numpy.ndarray)` for the selected frequency values.
    """
    mask = (frequency_values > low) & (frequency_values < high)
    return amplitude_values[mask], frequency_values[mask]
