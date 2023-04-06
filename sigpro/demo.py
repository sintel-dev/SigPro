"""Functions to load demo data."""

import json
import os
import random

import numpy as np
import pandas as pd
from scipy.signal import stft

DEMO_PATH = os.path.join(os.path.dirname(__file__), 'data')


def _load_demo(nrows=None):
    demo_path = os.path.join(DEMO_PATH, 'demo_timeseries.csv')
    df = pd.read_csv(demo_path, parse_dates=['timestamp'], nrows=nrows)
    df['sampling_frequency'] = 1000
    df["values"] = df["values"].apply(json.loads).apply(list)

    return df


def get_demo_data(nrows=None):
    """Get a demo ``pandas.DataFrame`` containing the accepted data format.

    Args:
        nrows (int):
            Number of rows to load from the demo datasets.

    Returns:
        A ``pd.DataFrame`` containing as ``values`` the signal values.
    """
    df = _load_demo(nrows)
    df = df.explode('values').reset_index(drop=True)

    time_delta = pd.to_timedelta(list(range(400)) * 750, 's')
    df['timestamp'] = df['timestamp'] + time_delta
    return df


def get_demo_primitives():
    """Get a dict of demo transformation and aggregation primitives.

    Returns:
        A tuple containing the list of transformation primitives and
        the list aggregation primitives
    """
    transformations = [
        {
            "name": "fft",
            "primitive": "sigpro.transformations.frequency.fft.fft"
        }
    ]
    aggregations = [
        {
            "name": "mean",
            "primitive": "sigpro.aggregations.amplitude.statistical.mean"
        },
        {
            "name": "std",
            "primitive": "sigpro.aggregations.amplitude.statistical.std"
        }
    ]

    return transformations, aggregations


def get_amplitude_demo(index=None):
    """Get amplitude values and sampling frequency used.

    The amplitude demo data is meant to be used for the any ``transformation`` functions
    that recieve as an input ``amplitude_values`` and ``sampling_frequency``.

    This amplitude values are loaded from the demo data without any transformations
    being applied to those values. There are `750` different signals. You can specify
    the desired index in order to retrive the same signal over and over, otherwise it
    will return a random signal.

    Args:
        index (int or None):
            If `int`, return the value at that index if `None` return a random index.

    Returns:
        tuple:
            A tuple with a `np.array` containing amplitude values and as second element the
            sampling frequency used.
    """
    df = _load_demo()
    if index is None:
        index = random.randint(0, len(df))

    return np.array(df.iloc[index]['values']), 10000


def get_frequency_demo(index=None, real=True):
    """Get amplitude values and the corresponding frequency values.

    The frequency demo data is meant to be used for the ``frequency aggregations``
    functions that recieve as an input ``amplitude_values`` and ``frequency_values``.

    This amplitude values are loaded from the demo data with ``fft`` transformations
    being applied to those values. There are `750` different signals. You can specify
    the desired index in order to retrive the same signal over and over, otherwise it
    will return a random signal.

    Args:
        index (int or None):
            If `int`, return the value at that index if `None` return a random index.
        real (bool):
            If ``True``, return the real values for the computed ``fft`` transformations,
            if it's set to ``False`` it will return a complex ndarray. Defaults to ``True``.

    Returns:
        tuple:
            A tuple two `np.array` containing amplitude values and frequency values.
    """
    amplitude_values, sampling_frequency = get_amplitude_demo(index)
    fft_values = np.fft.fft(amplitude_values)
    length = len(fft_values)
    frequencies = np.fft.fftfreq(len(fft_values), 1 / sampling_frequency)
    if real:
        fft_values = np.real(fft_values)

    return fft_values[0:length // 2], frequencies[0:length // 2]


def get_frequency_time_demo(index=None, real=True):
    """Get amplitude values, frequency values and time values.

    The frequency time demo data is meant to be used for the ``frequency time aggregations``
    functions that recieve as an input ``amplitude_values``, ``frequency_values`` and
    ``time_values``.

    This amplitude values are loaded from the demo data with ``fft`` transformations
    being applied to those values then a ``stft`` is being computed. There are `750`
    different signals. You can specify the desired index in order to retrive the same
    signal over and over, otherwise it will return a random signal.

    Args:
        index (int or None):
            If `int`, return the value at that index if `None` return a random index.
        real (bool):
            If ``True``, return the real values for the computed ``stft`` transformations,
            if it's set to ``False`` it will return a complex ndarray. Defaults to ``True``.

    Returns:
        tuple:
            A tuple two `np.array` containing amplitude values and frequency values.
    """
    amplitude_values, sampling_frequency = get_amplitude_demo(index)
    sample_frequencies, time_values, amplitude_values = stft(
        amplitude_values,
        fs=sampling_frequency
    )

    if real:
        amplitude_values = np.real(amplitude_values)

    return amplitude_values, sample_frequencies, time_values
