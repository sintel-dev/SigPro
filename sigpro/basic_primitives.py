"""Reference class implementations of existing primitives."""
from sigpro import primitive

###### Transformations
#### Amplitude

class Identity(primitive.AmplitudeTransformation):
    def __init__(self):
        super().__init__('sigpro.transformations.amplitude.identity.identity')

class PowerSpectrum(primitive.AmplitudeTransformation):
    def __init__(self):
        super().__init__('sigpro.transformations.amplitude.spectrum.power_spectrum')
        primitive_spec = contributing._get_primitive_spec('transformation', 'frequency')
        self.set_primitive_inputs(primitive_spec['args'])
        self.set_primitive_outputs(primitive_spec['output'])

#### Frequency

class FFT(primitive.FrequencyTransformation):
    def __init__(self):
        super().__init__("sigpro.transformations.frequency.fft.fft")

#Initialization: FFT()

class FFTReal(primitive.FrequencyTransformation):
    def __init__(self):
        super().__init__("sigpro.transformations.frequency.fft.fft_real")

#Initialization: FFTReal()
class FrequencyBand(primitive.FrequencyTransformation):

    def __init__(self, low, high):
        super.__init__("sigpro.transformations.frequency.band.frequency_band", init_params =  {'low': low, 'high': high})
        self.set_primitive_inputs([{"name": "amplitude_values", "type": "numpy.ndarray"}, {"name": "frequency_values", "type": "numpy.ndarray"} ])
        self.set_primitive_outputs([{'name': 'amplitude_values', 'type': "numpy.ndarray" }, {'name': 'frequency_values', 'type': "numpy.ndarray" }])
        self.set_fixed_hyperparameters({'low': {'type': 'int'}, 'high': {'type': 'int'}})
        
#Initialization: FrequencyBand(20,30) 


#### Frequency-time

class STFT(primitive.FrequencyTimeTransformation):
    def __init__(self):
        super().__init__('sigpro.transformations.frequency.stft.stft')
        self.set_primitive_outputs([ { "name": "amplitude_values", "type": "numpy.ndarray" }, { "name": "frequency_values", "type": "numpy.ndarray" }, { "name": "time_values", "type": "numpy.ndarray" } ])

#Initialization: STFT()


class STFTReal(primitive.FrequencyTimeTransformation):
    def __init__(self):
        super().__init__('sigpro.transformations.frequency.stft.stft_real')
        self.set_primitive_outputs([ { "name": "real_amplitude_values", "type": "numpy.ndarray" }, { "name": "frequency_values", "type": "numpy.ndarray" }, { "name": "time_values", "type": "numpy.ndarray" } ])

#Initialization: STFTReal()

####### Aggregations

####Amplitude
##Statistical


class CrestFactor(primitive.AmplitudeAggregation):
    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.crest_factor')
        self.set_primitive_outputs([{'name': 'crest_factor_value', 'type': "float" }])
#Initialization: CrestFactor()

class Kurtosis(primitive.AmplitudeAggregation):
    def __init__(self, fisher = True, bias = True):
        super().__init__('sigpro.aggregations.amplitude.statistical.kurtosis', init_params = {'fisher': fisher, 'bias': bias})
        self.set_primitive_outputs([{'name': 'kurtosis_value', 'type': "float" }])
        self.set_fixed_hyperparameters({'fisher': {'type': 'bool', 'default': True }, 'bias': {'type': 'bool', 'default': True}})

#Initialization: Kurtosis(True, False)

class Mean(primitive.AmplitudeAggregation):
    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.mean')
        self.set_primitive_outputs([{'name': 'mean_value', 'type': "float" }])

#Initialization: Mean()

class RMS(primitive.AmplitudeAggregation):
    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.rms')
        self.set_primitive_outputs([{'name': 'rms_value', 'type': "float" }])

#Initialization: RMS()

class Skew(primitive.AmplitudeAggregation):
    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.skew')
        self.set_primitive_outputs([{'name': 'skew_value', 'type': "float" }])

#Initialization: Skew()

class Std(primitive.AmplitudeAggregation):
    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.std')
        self.set_primitive_outputs([{'name': 'std_value', 'type': "float" }])

#Initialization: Std()

class Var(primitive.AmplitudeAggregation):
    def __init__(self):
        super().__init__('sigpro.aggregations.amplitude.statistical.var')
        self.set_primitive_outputs([{'name': 'var_value', 'type': "float" }])

#Initialization: Var()

####Frequency
##Spectral

class BandMean(primitive.FrequencyAggregation):
    def __init__(self, min_frequency, max_frequency):
        super().__init__('sigpro.aggregations.frequency.band.band_mean', init_params = {'min_frequency': min_frequency, 'max_frequency': max_frequency})
        self.set_fixed_hyperparameters({'min_frequency': {'type': 'float' }, 'max_frequency': {'type': 'float'}})

#Initialization: BandMean(20,30)