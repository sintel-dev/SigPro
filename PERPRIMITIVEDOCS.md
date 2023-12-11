# Per-Primitive Docs

Currently, the available primitives are as follows:

```python

['sigpro.SigPro',
 'sigpro.aggregations.amplitude.statistical.crest_factor',
 'sigpro.aggregations.amplitude.statistical.kurtosis', 
 'sigpro.aggregations.amplitude.statistical.mean', 
 'sigpro.aggregations.amplitude.statistical.rms', 
 'sigpro.aggregations.amplitude.statistical.skew',  
 'sigpro.aggregations.amplitude.statistical.std',
 'sigpro.aggregations.amplitude.statistical.var', 
 'sigpro.aggregations.frequency.band.band_mean',
 'sigpro.transformations.amplitude.identity.identity', 
 'sigpro.transformations.amplitude.spectrum.power_spectrum',
 'sigpro.transformations.frequency.band.frequency_band', 
 'sigpro.transformations.frequency.fft.fft', 
 'sigpro.transformations.frequency.fft.fft_real', 
 'sigpro.transformations.frequency_time.stft.stft', 
 'sigpro.transformations.frequency_time.stft.stft_real']
```

## sigpro.SigPro

**path**: `sigpro.SigPro`

**description** : Please see the SigPro page for more detailed documentation.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| See pipeline documentation |  |  |
| hyperparameters |  |  |
| keep_columns | bool, list | If bool, whether to keep non-feature columns. If list, keep the columns in the list. |
| values_column_name | str | Name of signal values column in input. |
| transformations | list | List of transformations to apply sequentially before applying aggregations in parallel. |
| aggregations | list | List of aggregations to apply in parallel after all transformations are applied (in sequence).  |
| input_is_dataframe | bool | Whether the input is a pandas DataFrame. Defaults to True. |
| output |  |  |
| See Documentation |  |  |

## sigpro.transformations.amplitude.identity.identity

**path**: `sigpro.transformations.amplitude.identity.identity`

**description** : This primitive simply returns the input amplitude values as its output.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| amplitude_values | numpy.ndarray | Output (identity) signal amplitude values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([[1,2,3,4,5]])
transformed_data = run_primitive(
    'sigpro.transformations.amplitude.identity.identity',
    amplitude_values= data
)
transformed_data
```

## sigpro.transformations.amplitude.spectrum.power_spectrum

**path**: `sigpro.transformations.amplitude.spectrum.power_spectrum`

**description** : This primitive applies an RFFT on the amplitude values and return the real components.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| sampling_frequency | int, float | Sampling frequency value passed in Hz. |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| amplitude_values | numpy.ndarray | Output real components |
| frequency_values | numpy.ndarray | Frequency values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([[1,2,3,4,5]])
frequency = 1000
transformed_data = run_primitive(
    'sigpro.transformations.amplitude.spectrum.power_spectrum',
    amplitude_values= data,
		sampling_frequency = frequency
)
transformed_data, freq_values
```

## sigpro.transformations.frequency.band.frequency_band

**path**: `sigpro.transformations.frequency.band.frequency_band`

**description** : This primitive filters between a high and low band frequency and return the amplitude values and frequency values for those.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| frequency_values | numpy.ndarray | Input frequency values passed in Hz. |
| hyperparameters |  |  |
| low | int | Lower band frequency |
| high | int | Higher band frequency |
| output |  |  |
| amplitude_values | numpy.ndarray | Output real components |
| frequency_values | numpy.ndarray | Frequency values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([[1,2,3,4,5]])
frequency_values = np.array([[70,140,210, 280, 350]])
transformed_data, freq_values = run_primitive(
    'sigpro.transformations.frequency.band.frequency_band',
    amplitude_values= data,
	frequency_values = frequency_values,
    low = 100, 
    high = 300
)
transformed_data, freq_values,
```

## sigpro.transformations.frequency.fft.fft

**path**: `sigpro.transformations.frequency.fft.fft`

**description** : This primitive applies an FFT on the amplitude values using the discrete Fourier transform in `numpy`. 

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| sampling_frequency | int, float | Sampling frequency value passed in Hz. |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| amplitude_values | numpy.ndarray | Output all components |
| frequency_values | numpy.ndarray | Frequency values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([[1,2,3,4,5]])
frequency = 1000
transformed_data, freq_values = run_primitive(
    'sigpro.transformations.frequency.fft.fft',
    amplitude_values= data,
		sampling_frequency = frequency

)
transformed_data, freq_values
```

## sigpro.transformations.frequency.fft.fft_real

**path**: `sigpro.transformations.frequency.fft.fft_real`

**description** : This primitive applies an FFT on the amplitude values using the discrete Fourier transform in `numpy` and returns the real components.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| sampling_frequency | int, float | Sampling frequency value passed in Hz. |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| amplitude_values | numpy.ndarray | Output real components of FFT |
| frequency_values | numpy.ndarray | Frequency values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([[1,2,3,4,5]])
frequency = 1000
transformed_data, freq_values = run_primitive(
    'sigpro.transformations.frequency.fft.fft_real',
    amplitude_values= data,
		sampling_frequency = frequency

)
transformed_data, freq_values
```

## sigpro.transformations.frequency_time.stft.stft

**path**: `sigpro.transformations.frequency.stft.stft`

**description** : This primitive computes and returns the short time Fourier transform.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| sampling_frequency | int, float | Sampling frequency value passed in Hz. |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| amplitude_values | numpy.ndarray | Output all components of STFT |
| frequency_values | numpy.ndarray | Frequency values |
| time_values | numpy.ndarray | Time values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([[1,2,3,4,5]])
frequency = 1000
transformed_data, freq_values, time_values = run_primitive(
    'sigpro.transformations.frequency_time.stft.stft', #note: this is inconsistent
    amplitude_values= data,
		sampling_frequency = frequency

)
transformed_data, freq_values, time_values 
```

## sigpro.transformations.frequency_time.stft.stft_real

**path**: `sigpro.transformations.frequency.stft.stft_real`

**description** : This primitive computes and returns the real part of the short time Fourier transform.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| sampling_frequency | int, float | Sampling frequency value passed in Hz. |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| amplitude_values | numpy.ndarray | Output real components of STFT |
| frequency_values | numpy.ndarray | Frequency values |
| time_values | numpy.ndarray | Time values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([[1,2,3,4,5]])
frequency = 1000
transformed_data, freq_values, time_values = run_primitive(
    'sigpro.transformations.frequency_time.stft.stft_real', #note: this is inconsistent
    amplitude_values= data,
		sampling_frequency = frequency

)
transformed_data, freq_values, time_values 
```

## sigpro.aggregation.amplitude.statistical.mean

**path**: `sigpro.aggregation.amplitude.statistical.mean`

**description** : This primitive computes and returns the arithmetic mean of the input values.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| mean_value | float | Output mean of amplitude values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([1,2,3,4,5])
output = run_primitive(
    'sigpro.aggregations.amplitude.statistical.mean', 
    amplitude_values= data,
)
output
```

## sigpro.aggregation.amplitude.statistical.std

**path**: `sigpro.aggregation.amplitude.statistical.std`

**description** : This primitive computes and returns the standard deviation of the input values.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| std_value | float | Output standard deviation of amplitude values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([1,2,3,4,5])
output = run_primitive(
    'sigpro.aggregations.amplitude.statistical.std', 
    amplitude_values= data,
)
output
```

## sigpro.aggregation.amplitude.statistical.kurtosis

**path**: `sigpro.aggregation.amplitude.statistical.std`

**description** : This primitive computes and returns the kurtosis of the input values.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| hyperparameters |  |  |
| fisher | bool | If True (default), use Fisher definition (normal 0.0). If False, use Pearson definition (normal 3.0). |
| bias | bool | If False, correct calculations for statistical bias. Defaults to True. |
| output |  |  |
| kurtosis_value | float | Output kurtosis of amplitude values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([1,2,3,4,5])
output = run_primitive(
    'sigpro.aggregations.amplitude.statistical.kurtosis', 
    amplitude_values= data,
		fisher = True,
		bias = True
)
output
```

## sigpro.aggregation.amplitude.statistical.var

**path**: `sigpro.aggregation.amplitude.statistical.var`

**description** : This primitive computes and returns the variance of the input values.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| var_value | float | Output variance of amplitude values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([1,2,3,4,5])
output = run_primitive(
    'sigpro.aggregations.amplitude.statistical.var', 
    amplitude_values= data,
)
output
```

## sigpro.aggregation.amplitude.statistical.rms

**path**: `sigpro.aggregation.amplitude.statistical.rms`

**description** : This primitive computes and returns the root mean square (RMS) of the input values.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| rms_value | float | Output RMS of amplitude values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([1,2,3,4,5])
output = run_primitive(
    'sigpro.aggregations.amplitude.statistical.rms', 
    amplitude_values= data,
)
output
```

## sigpro.aggregation.amplitude.statistical.skew

**path**: `sigpro.aggregation.amplitude.statistical.skew`

**description** : This primitive computes and returns the skew of the input values.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| skew_value | float | Output skew of amplitude values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([1,2,3,4,5])
output = run_primitive(
    'sigpro.aggregations.amplitude.statistical.skew', 
    amplitude_values= data,
)
output
```

## sigpro.aggregation.amplitude.statistical.crest_factor

**path**: `sigpro.aggregation.amplitude.statistical.crest_factor`

**description** : This primitive computes and returns the crest factor (ratio of peak to RMS) of the input values.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| hyperparameters |  |  |
| N/A |  |  |
| output |  |  |
| crest_factor_value | float | Output crest factor of amplitude values |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([1,2,3,4,5])
output = run_primitive(
    'sigpro.aggregations.amplitude.statistical.crest_factor', 
    amplitude_values= data,
)
output
```

## sigpro.aggregations.frequency.band.band_mean

**path**: `sigpro.aggregations.frequency.band.band_mean`

**description** : This primitive filters between a high and low band and computes the mean value for this specific band.

| argument | type | description |
| --- | --- | --- |
| parameters |  |  |
| amplitude_values | numpy.ndarray | Input signal amplitude values |
| frequency_values | numpy.ndarray | Input frequency values passed in Hz. |
| hyperparameters |  |  |
| min_frequency | float | Lower band threshold. |
| max_frequency | float | Upper band threshold. |
| output |  |  |
| value | float | Output mean of amplitude values within frequency band. |

```python
import numpy as np
from sigpro.contributing import run_primitive

data = np.array([[1,2,3,4,5]])
frequency_values = np.array([[70,140,210, 280, 350]])
output = run_primitive(
    'sigpro.aggregations.frequency.band.band_mean',
    amplitude_values= data,
	frequency_values = frequency_values,
    min_frequency = 100, 
    max_frequency = 300
)
output
```
