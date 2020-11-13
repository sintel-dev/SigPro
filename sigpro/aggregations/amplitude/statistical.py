"""Amplitude statistical module."""

import numpy as np
import scipy.stats


def mean(amplitude_values):
    """Calculate the mean value of the values.

    Args:
        amplitude_values (numpy.ndarray):
            Array of floats representing signal values.

    Returns:
       float:
           `mean` value of the input array.
    """
    return np.mean(amplitude_values)


def std(amplitude_values):
    """Compute the arithmetic mean value of the values.

    Args:
        amplitude_values (numpy.ndarray):
            Array of floats representing signal values.

    Returns:
       float:
           `std` value of the input array.
    """
    return np.std(amplitude_values)


def var(amplitude_values):
    """Compute the variance value of the values.

    Args:
        amplitude_values (numpy.ndarray):
            Array of floats representing signal values.

    Returns:
       float:
           `std` value of the input array.
    """
    return np.var(amplitude_values)


def rms(amplitude_values):
    """Compute the RMS (Root Mean Square) of the values.

    Args:
        amplitude_values (numpy.ndarray):
            Array of floats representing signal values.

    Returns:
       float:
           RMS of the input array.
    """
    return np.sqrt((np.array(amplitude_values) ** 2).mean())


def crest_factor(amplitude_values):
    """Compute the ratio of the peak to the RMS.

    Used for estimating the amount of impact wear in a bearing.

    Args:
        amplitude_values (numpy.ndarray):
            Array of floats representing signal values.

    Returns:
        float:
            The crest factor of the inputted values.
    """
    peak = max(np.abs(amplitude_values))
    return peak / rms(amplitude_values)


def skew(amplitude_values):
    """Compute the sample skewness of an array of values.

    Args:
        amplitude_values (numpy.ndarray):
            Array of floats representing signal values.

    Returns:
       float:
           The skewness value of the input array.
    """
    return scipy.stats.skew(amplitude_values)


def kurtosis(amplitude_values, fisher=True, bias=True):
    """Compute the kurtosis ,Fisher or Pearson, of an array of values.

    Args:
        amplitude_values (numpy.ndarray):
            Array of floats representing signal values.
        fisher (bool):
            If ``True``, Fisher’s definition is used (normal ==> 0.0). If ``False``,
            Pearson’s definition is used (normal ==> 3.0). Defaults to ``True``.
        bias (bool):
            If ``False``, then the calculations are corrected for statistical bias.
            Defaults to ``True``.

    Returns:
       float:
           The kurtosis value of the input array. If all values are equal, return
           `-3` for Fisher's definition and `0` for Pearson's definition.
    """
    return scipy.stats.kurtosis(amplitude_values, fisher=fisher, bias=bias)
