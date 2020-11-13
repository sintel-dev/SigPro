"""Test identity module."""

from sigpro.transformations.amplitude.identity import identity


def test_identity():
    values = list(range(20))
    result = identity(values.copy())
    assert values == result
