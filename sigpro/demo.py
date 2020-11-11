"""Functions to load demo data."""

import json
import os
import random

import numpy as np
import pandas as pd
from scipy.signal import stft

DEMO_PATH = os.path.join(os.path.dirname(__file__), 'data')


def get_demo_data():
    """Get a demo ``pandas.DataFrame`` containing the accepted data format.

    Returns:
        A ``pd.DataFrame`` containing as ``values`` the signal values.
    """
    demo_path = os.path.join(DEMO_PATH, 'demo_timeseries.csv')
    df = pd.read_csv(demo_path, parse_dates=['timestamp'])
    df["values"] = df["values"].apply(json.loads).apply(list)
    return df


def get_amplitude_demo(idx=None):
    """Get amplitude values and sampling frequency used.

    The amplitude demo data is meant to be used for the any ``transformation`` functions
    that recieve as an input ``amplitude_values`` and ``sampling_frequency``.

    This amplitude values are loaded from the demo data without any transformations
    being applied to those values. There are `750` different signals. You can specify
    the desired index in order to retrive the same signal over and over, otherwise it
    will return a random signal.

    Args:
        idx (int or None):
            If `int`, return the value at that index if `None` return a random index.

    Returns:
        tuple:
            A tuple with a `np.array` containing amplitude values and as second element the
            sampling frequency used.
    """
    df = get_demo_data()
    if idx is None:
        idx = random.randint(0, len(df))

    return np.array(df.iloc[idx]['values']), 10000


def get_frequency_demo(idx=None):
    """Get amplitude values and the corresponding frequency values.

    The frequency demo data is meant to be used for the ``frequency aggregations``
    functions that recieve as an input ``amplitude_values`` and ``frequency_values``.

    This amplitude values are loaded from the demo data with ``fft`` transformations
    being applied to those values. There are `750` different signals. You can specify
    the desired index in order to retrive the same signal over and over, otherwise it
    will return a random signal.

    Args:
        idx (int or None):
            If `int`, return the value at that index if `None` return a random index.

    Returns:
        tuple:
            A tuple two `np.array` containing amplitude values and frequency values.
    """
    amplitude_values, sampling_frequency = get_amplitude_demo(idx)
    fft_values = np.fft.fft(amplitude_values)
    frequencies = np.fft.fftfreq(len(fft_values), sampling_frequency)
    return fft_values, frequencies


def get_frequency_time_demo(idx=None):
    """Get amplitude values, frequency values and time values.

    The frequency time demo data is meant to be used for the ``frequency time aggregations``
    functions that recieve as an input ``amplitude_values``, ``frequency_values`` and
    ``time_values``.

    This amplitude values are loaded from the demo data with ``fft`` transformations
    being applied to those values then a ``stft`` is being computed. There are `750`
    different signals. You can specify the desired index in order to retrive the same
    signal over and over, otherwise it will return a random signal.

    Args:
        idx (int or None):
            If `int`, return the value at that index if `None` return a random index.

    Returns:
        tuple:
            A tuple two `np.array` containing amplitude values and frequency values.
    """
    amplitude_values, sampling_frequency = get_amplitude_demo(idx)
    sample_frequencies, time_values, amplitude_values = stft(
        amplitude_values,
        fs=sampling_frequency
    )

    return amplitude_values, sample_frequencies, time_values
