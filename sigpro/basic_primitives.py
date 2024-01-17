# -*- coding: utf-8 -*-
"""Reference class implementations of existing primitives."""
from sigpro import contributing, primitive

# Transformations


class Identity(primitive.AmplitudeTransformation):
    """Identity primitive class."""

    def __init__(self):
        super().__init__('sigpro.transformations.amplitude.identity.identity')


class PowerSpectrum(primitive.AmplitudeTransformation):
    """PowerSpectrum primitive class."""

    def __init__(self):
        super().__init__('sigpro.transformations.amplitude.spectrum.power_spectrum')
        primitive_spec = contributing._get_primitive_spec('transformation', 'frequency')
        self.set_primitive_inputs(primitive_spec['args'])
        self.set_primitive_outputs(primitive_spec['output'])


class FFT(primitive.FrequencyTransformation):
    """FFT primitive class."""

    def __init__(self):
        super().__init__("sigpro.transformations.frequency.fft.fft")


class FFTReal(primitive.FrequencyTransformation):
    """FFTReal primitive class."""

    def __init__(self):
        super().__init__("sigpro.transformations.frequency.fft.fft_real")


class FrequencyBand(primitive.FrequencyTransformation):
    """FrequencyBand primitive class."""

    def __init__(self, low, high):
        super().__init__("sigpro.transformations.frequency.band.frequency_band",
                         init_params={'low': low, 'high': high})
        self.set_primitive_inputs([{"name": "amplitude_values", "type": "numpy.ndarray"},
                                   {"name": "frequency_values", "type": "numpy.ndarray"}])
        self.set_primitive_outputs([{'name': 'amplitude_values', 'type': "numpy.ndarray"},
                                    {'name': 'frequency_values', 'type': "numpy.ndarray"}])
        self.set_fixed_hyperparameters({'low': {'type': 'int'}, 'high': {'type': 'int'}})


class STFT(primitive.FrequencyTimeTransformation):
    """STFT primitive class."""

    def __init__(self):
        super().__init__('sigpro.transformations.frequency.stft.stft')
        self.set_primitive_outputs([{"name": "amplitude_values", "type": "numpy.ndarray"},
                                    {"name": "frequency_values", "type": "numpy.ndarray"},
                                    {"name": "time_values", "type": "numpy.ndarray"}])


class STFTReal(primitive.FrequencyTimeTransformation):
    """STFTReal primitive class."""

    def __init__(self):
        super().__init__('sigpro.transformations.frequency.stft.stft_real')
        self.set_primitive_outputs([{"name": "real_amplitude_values", "type": "numpy.ndarray"},
                                    {"name": "frequency_values", "type": "numpy.ndarray"},
                                    {"name": "time_values", "type": "numpy.ndarray"}])

# Aggregations


class CrestFactor(primitive.AmplitudeAggregation):
    """CrestFactor primitive class."""

    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.crest_factor')
        self.set_primitive_outputs([{'name': 'crest_factor_value', 'type': "float"}])


class Kurtosis(primitive.AmplitudeAggregation):
    """Kurtosis primitive class."""

    def __init__(self, fisher=True, bias=True):
        super().__init__('sigpro.aggregations.amplitude.statistical.kurtosis',
                         init_params={'fisher': fisher, 'bias': bias})
        self.set_primitive_outputs([{'name': 'kurtosis_value', 'type': "float"}])
        self.set_fixed_hyperparameters({'fisher': {'type': 'bool', 'default': True},
                                        'bias': {'type': 'bool', 'default': True}})


class Mean(primitive.AmplitudeAggregation):
    """Mean primitive class."""

    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.mean')
        self.set_primitive_outputs([{'name': 'mean_value', 'type': "float"}])


class RMS(primitive.AmplitudeAggregation):
    """RMS primitive class."""

    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.rms')
        self.set_primitive_outputs([{'name': 'rms_value', 'type': "float"}])


class Skew(primitive.AmplitudeAggregation):
    """Skew primitive class."""

    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.skew')
        self.set_primitive_outputs([{'name': 'skew_value', 'type': "float"}])


class Std(primitive.AmplitudeAggregation):
    """Std primitive class."""

    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.std')
        self.set_primitive_outputs([{'name': 'std_value', 'type': "float"}])


class Var(primitive.AmplitudeAggregation):
    """Var primitive class."""

    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.var')
        self.set_primitive_outputs([{'name': 'var_value', 'type': "float"}])


class BandMean(primitive.FrequencyAggregation):
    """BandMean primitive class."""

    def __init__(self, min_frequency, max_frequency):
        super().__init__('sigpro.aggregations.frequency.band.band_mean', init_params={
            'min_frequency': min_frequency, 'max_frequency': max_frequency})
        self.set_fixed_hyperparameters({'min_frequency': {'type': 'float'},
                                        'max_frequency': {'type': 'float'}})
