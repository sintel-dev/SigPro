# -*- coding: utf-8 -*-

"""Tests for sigpro.aggregations.frequency.band package."""

import numpy as np

from sigpro.aggregations.frequency.band import band_mean

AMPLITUDE_VALUES = np.arange(200)
FREQUENCY_VALUES = np.arange(200)


def test_band_mean():
    # setup
    expected = 15  # we computed previoulsy

    # run
    result = band_mean(AMPLITUDE_VALUES, FREQUENCY_VALUES, min_frequency=10, max_frequency=20)

    # assert
    assert result == expected
