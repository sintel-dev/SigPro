"""Test module for SigPro primitive and basic_primitives modules."""

from sigpro import basic_primitives, primitive


def test_basic_primitives():
    """Test basic_primitives module."""

    identity = basic_primitives.Identity()
    power_spectrum = basic_primitives.PowerSpectrum()
    assert isinstance(identity, primitive.Primitive)
    assert isinstance(power_spectrum, primitive.Primitive)
    assert identity.get_type_subtype() == ('transformation', 'amplitude')
    assert power_spectrum.get_type_subtype() == ('transformation', 'amplitude')

    fft = basic_primitives.FFT()
    fft_real = basic_primitives.FFTReal()

    assert isinstance(fft, primitive.Primitive)
    assert isinstance(fft_real, primitive.Primitive)
    assert fft.get_type_subtype() == ('transformation', 'frequency')
    assert fft_real.get_type_subtype() == ('transformation', 'frequency')

    std = basic_primitives.Std()
    var = basic_primitives.Var()
    assert isinstance(std, primitive.Primitive)
    assert isinstance(var, primitive.Primitive)
    assert std.get_type_subtype() == ('aggregation', 'amplitude')
    assert var.get_type_subtype() == ('aggregation', 'amplitude')

    band_mean = basic_primitives.BandMean(min_frequency=0, max_frequency=100)
    assert isinstance(band_mean, primitive.Primitive)
    assert band_mean.get_type_subtype() == ('aggregation', 'frequency')


def test_primitives():
    """Test primitives module."""

    kurtosis = basic_primitives.Kurtosis(bias=False)
    kurtosis.set_tag('kurtosis_test')
    primitive_str = 'sigpro.aggregations.amplitude.statistical.kurtosis'
    init_params = {'fisher': True, 'bias': False}
    assert kurtosis.get_hyperparam_dict() == {'name': 'kurtosis_test',
                                              'primitive': primitive_str,
                                              'init_params': init_params}

    frequency_band = basic_primitives.FrequencyBand(low=10, high=50)
    frequency_band.set_tag('frequency_band_test')
    primitive_str = 'sigpro.transformations.frequency.band.frequency_band'
    init_params = {'low': 10, 'high': 50}
    assert frequency_band.get_hyperparam_dict() == {'name': 'frequency_band_test',
                                                    'primitive': primitive_str,
                                                    'init_params': init_params}
