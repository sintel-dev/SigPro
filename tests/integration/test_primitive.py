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
    identity.make_primitive_json()
    power_spectrum.make_primitive_json()

    fft = basic_primitives.FFT()
    fft_real = basic_primitives.FFTReal()

    assert isinstance(fft, primitive.Primitive)
    assert isinstance(fft_real, primitive.Primitive)
    assert fft.get_type_subtype() == ('transformation', 'frequency')
    assert fft_real.get_type_subtype() == ('transformation', 'frequency')
    fft.make_primitive_json()
    fft_real.make_primitive_json()

    frequency_band = basic_primitives.FrequencyBand(low=10, high=20)
    assert isinstance(frequency_band, primitive.Primitive)
    assert frequency_band.get_type_subtype() == ('transformation', 'frequency')
    frequency_band.make_primitive_json()

    stft = basic_primitives.STFT()
    stft_real = basic_primitives.STFTReal()
    assert isinstance(stft, primitive.Primitive)
    assert isinstance(stft_real, primitive.Primitive)
    assert stft.get_type_subtype() == ('transformation', 'frequency_time')
    assert stft_real.get_type_subtype() == ('transformation', 'frequency_time')
    stft.make_primitive_json()
    stft_real.make_primitive_json()

    std = basic_primitives.Std()
    var = basic_primitives.Var()
    rms = basic_primitives.RMS()
    cf = basic_primitives.CrestFactor()
    skew = basic_primitives.Skew()
    assert isinstance(std, primitive.Primitive)
    assert isinstance(var, primitive.Primitive)
    assert isinstance(rms, primitive.Primitive)
    assert isinstance(cf, primitive.Primitive)
    assert isinstance(skew, primitive.Primitive)
    assert std.get_type_subtype() == ('aggregation', 'amplitude')
    assert var.get_type_subtype() == ('aggregation', 'amplitude')
    assert rms.get_type_subtype() == ('aggregation', 'amplitude')
    assert cf.get_type_subtype() == ('aggregation', 'amplitude')
    assert skew.get_type_subtype() == ('aggregation', 'amplitude')
    std.make_primitive_json()
    var.make_primitive_json()
    rms.make_primitive_json()
    cf.make_primitive_json()
    skew.make_primitive_json()

    band_mean = basic_primitives.BandMean(min_frequency=0, max_frequency=100)
    assert isinstance(band_mean, primitive.Primitive)
    assert band_mean.get_type_subtype() == ('aggregation', 'frequency')
    band_mean.make_primitive_json()


def test_primitives():
    """Test primitives module."""

    kurtosis = basic_primitives.Kurtosis(bias=False)
    kurtosis.set_tag('kurtosis_test')
    primitive_str = 'sigpro.aggregations.amplitude.statistical.kurtosis'
    init_params = {'fisher': True, 'bias': False}
    assert kurtosis.get_hyperparam_dict() == {'name': 'kurtosis_test',
                                              'primitive': primitive_str,
                                              'init_params': init_params}
    kurtosis.make_primitive_json()
    frequency_band = basic_primitives.FrequencyBand(low=10, high=50)
    frequency_band.set_tag('frequency_band_test')
    primitive_str = 'sigpro.transformations.frequency.band.frequency_band'
    init_params = {'low': 10, 'high': 50}
    assert frequency_band.get_hyperparam_dict() == {'name': 'frequency_band_test',
                                                    'primitive': primitive_str,
                                                    'init_params': init_params}
