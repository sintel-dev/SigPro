"""Test module for SigPro primitive and basic_primitives modules."""

from sigpro import basic_primitives, primitive


def test_basic_primitives():
    """Test basic_primitives module."""

    identity = basic_primitives.Identity()
    power_spectrum = basic_primitives.PowerSpectrum()
    assert isinstance(identity, primitive.Primitive)
    assert isinstance(power_spectrum, primitive.Primitive)
    assert identity.get_type_subtype() == ('transformation', 'frequency')
    assert power_spectrum.get_type_subtype() == ('transformation', 'frequency')


def test_primitives():
    """Test primitives module."""

    kurtosis = basic_primitives.Kurtosis(bias=False)
    kurtosis.set_tag('kurtosis_test')
    primitive_str = 'sigpro.aggregations.amplitude.statistical.kurtosis'
    init_params = {'fisher': True, 'bias': False}
    assert kurtosis.get_hyperparam_dict() == {'name': 'kurtosis_test',
                                              'primitive': primitive_str,
                                              'init_params': init_params}
