# -*- coding: utf-8 -*-

"""Tests for sigpro.aggregations.amplitude.statistical package."""

from sigpro.aggregations.amplitude.statistical import (
    crest_factor, kurtosis, mean, rms, skew, std, var)

VALUES = list(range(20))


def test_crest_factor():
    expected = 19. / 11.113055
    result = crest_factor(VALUES)
    assert round(result, 4) == round(expected, 4)


def test_rms():
    result = rms(VALUES)
    assert round(result, 6) == 11.113055


def test_mean():
    result = mean(VALUES)
    assert result == 9.5


def test_std():
    result = std(VALUES)
    assert round(result, 6) == 5.766281


def test_var():
    result = var(VALUES)
    assert result == 33.25


def test_skew():
    result = skew(VALUES)
    assert result == 0.0


def test_kurtosis_fisher():
    result = kurtosis(VALUES)
    assert round(result, 6) == -1.206015


def test_kurtosis_fisher_bias_false():
    result = kurtosis(VALUES, bias=False)
    assert result == -1.2


def test_kurtosis_pearson():
    result = kurtosis(VALUES, fisher=False)
    assert round(result, 6) == 1.793985


def test_kurtosis_pearson_bias_false():
    result = kurtosis(VALUES, fisher=False, bias=False)
    assert result == 1.8
