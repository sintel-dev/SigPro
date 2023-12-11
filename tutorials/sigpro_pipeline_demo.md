# Processing Signals with Pipelines

Now that we have identified and/or generated several primitives for our signal feature generation, we would like to define a reusable *pipeline* for doing so. 

First, let's import the required libraries and functions.



```python
import sigpro
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sigpro.demo import _load_demo as get_demo
```


## Defining Primitives

Recall that we can obtain the list of available primitives with the `get_primitives` method:



```python
from sigpro import get_primitives

get_primitives()
```




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



In addition, we can also define our own custom primitives.

## Building a Pipeline

Let’s go ahead and define a feature processing pipeline that sequentially applies the `identity`and `fft` transformations before applying the `std` aggregation. To pass these primitives into the signal processor, we must write each primitive as a dictionary with the following fields:

- `name`: Name of the transformation / aggregation.
- `primitive`: Name of the primitive to apply.
- `init_params`: Dictionary containing the initializing parameters for the primitive. *

Since we choose not to specify any initial parameters, we do not set `init_params` in these dictionaries.


```python
identity_transform = {'name': 'identity1',
            'primitive': 'sigpro.transformations.amplitude.identity.identity'}

fft_transform =  {'name': 'fft1',
            'primitive': 'sigpro.transformations.frequency.fft.fft'}

std_agg = {'name': 'std1',
            'primitive': "sigpro.aggregations.amplitude.statistical.std"}
```


We now define a new pipeline containing  the primitives we would like to apply. At minimum, we will need to pass in a list of transformations and a list of aggregations; the full list of available arguments is given below.

- Inputs:
    - `transformations (list)` : List of dictionaries containing the transformation primitives.
    - `aggregations (list)`:  List of dictionaries containing the aggregation primitives.
    - `values_column_name (str)`(optional):The name of the column that contains the signal values. Defaults to `'values'`.
    - `keep_columns (Union[bool, list])`  (optional): Whether to keep non-feature columns in the output DataFrame or not. If a list of column names are passed, those columns are kept. Defaults to `False`.
    - `input_is_dataframe (bool)` (optional): Whether the input is a pandas Dataframe. Defaults to `True`.

Returning to the example:


```python
transformations = [identity_transform, fft_transform]

aggregations = [std_agg]

mypipeline = sigpro.SigPro(transformations, aggregations, values_column_name = 'yvalues', keep_columns = True)
```


SigPro will proceed to build an `MLPipeline` that can be reused to build features.

To check that `mypipeline` was defined correctly, we can check the input and output arguments with the `get_input_args` and `get_output_args` methods.


```python
input_args = mypipeline.get_input_args()
output_args = mypipeline.get_output_args()

print(input_args)
print(output_args)
```

    [{'name': 'readings', 'keyword': 'data', 'type': 'pandas.DataFrame'}, {'name': 'feature_columns', 'default': None, 'type': 'list'}]
    [{'name': 'readings', 'type': 'pandas.DataFrame'}, {'name': 'feature_columns', 'type': 'list'}]


## Applying a Pipeline with `process_signal`

Once our pipeline is correctly defined, we apply the `process_signal` method to a demo dataset. Recall that `process_signal` is defined as follows:


```python
def process_signal(self, data=None, window=None, time_index=None, groupby_index=None,
                       feature_columns=None, **kwargs):

		...
		return data, feature_columns
```

`process_signal` accepts as input the following arguments:

- `data (pd.Dataframe)` : Dataframe with a column containing signal values.
- `window (str)`: Duration of window size, e.g. ('1h').
- `time_index (str)`: Name of column in `data` that represents the time index.
- `groupby_index (str or list[str])`: List of column names to group together and take the window over.
- `feature_columns (list)`: List of columns from the input data that should be considered as features (and not dropped).

`process_signal` outputs the following:

- `data (pd.Dataframe)`: Dataframe containing output feature values as constructed from the signal
- `feature_columns (list)`: list of (generated) feature names.

We now apply our pipeline to a toy dataset. We define our toy dataset as follows: 


```python
demo_dataset = get_demo()
demo_dataset.columns = ['turbine_id', 'signal_id', 'xvalues', 'yvalues', 'sampling_frequency']
demo_dataset.head()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>turbine_id</th>
      <th>signal_id</th>
      <th>xvalues</th>
      <th>yvalues</th>
      <th>sampling_frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>2020-01-01 00:00:00</td>
      <td>[0.43616983763682876, -0.17662312586241055, 0....</td>
      <td>1000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>2020-01-01 01:00:00</td>
      <td>[0.8023828754411122, -0.14122063493312714, -0....</td>
      <td>1000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>2020-01-01 02:00:00</td>
      <td>[-1.3143142430046044, -1.1055740033788437, -0....</td>
      <td>1000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>2020-01-01 03:00:00</td>
      <td>[-0.45981995520032104, -0.3255426061995603, -0...</td>
      <td>1000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>2020-01-01 04:00:00</td>
      <td>[-0.6380405111460377, -0.11924167777027689, 0....</td>
      <td>1000</td>
    </tr>
  </tbody>
</table>
</div>



Finally, we apply the `process_signal` method of our previously defined pipeline:


```python
processed_data, feature_columns = mypipeline.process_signal(demo_dataset, time_index = 'xvalues')

processed_data.head()

```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>turbine_id</th>
      <th>signal_id</th>
      <th>xvalues</th>
      <th>yvalues</th>
      <th>sampling_frequency</th>
      <th>identity1.fft1.std1.std_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>2020-01-01 00:00:00</td>
      <td>[0.43616983763682876, -0.17662312586241055, 0....</td>
      <td>1000</td>
      <td>14.444991</td>
    </tr>
    <tr>
      <th>1</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>2020-01-01 01:00:00</td>
      <td>[0.8023828754411122, -0.14122063493312714, -0....</td>
      <td>1000</td>
      <td>12.326223</td>
    </tr>
    <tr>
      <th>2</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>2020-01-01 02:00:00</td>
      <td>[-1.3143142430046044, -1.1055740033788437, -0....</td>
      <td>1000</td>
      <td>12.051415</td>
    </tr>
    <tr>
      <th>3</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>2020-01-01 03:00:00</td>
      <td>[-0.45981995520032104, -0.3255426061995603, -0...</td>
      <td>1000</td>
      <td>10.657243</td>
    </tr>
    <tr>
      <th>4</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>2020-01-01 04:00:00</td>
      <td>[-0.6380405111460377, -0.11924167777027689, 0....</td>
      <td>1000</td>
      <td>12.640728</td>
    </tr>
  </tbody>
</table>
</div>




Success! We have managed to apply the primitives to generate features on the input dataset.



```python

```
