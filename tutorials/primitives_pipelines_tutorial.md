# Using SigPro

In this notebook, we will walk through the process of defining and using primitives in SigPro.

## Primitives 
Feature engineering in `SigPro` centers around the **primitive**. In `SigPro`, primitives fall under two main types: transformations, and aggregations. Each type of primitive is further broken down into several primitive subtypes.

## Inheritance

All primitives are instances of the `sigpro.primitive.Primitive` base class. Furthermore, depending on their respective types and subtypes, each primitive inherits from a specific subclass. For example, a frequency-time transformation primitive would inherit from `sigpro.primitive.FrequencyTimeTransformation`, while an amplitude aggrigation would inherit from `sigpro.primitive.AmplitudeAggregation`.

### Initializing Primitives

Let's view a simple primitive and see how to use it.


```python
# Import primitive
from sigpro.basic_primitives import Mean

# Initialize the primitive object
mean_primitive = Mean()

mean_primitive
```




    <sigpro.basic_primitives.Mean at 0x7f91e078db50>



The `Mean` primitive we just defined is an example of an `AmplitudeAggregation`; in other words, its type is `'aggregation'`, and its subtype is `'amplitude'`. To see this, we call its `get_type_subtype` method:


```python
# Check the type and subtype of mean_primitive
mean_primitive.get_type_subtype()
```




    ('aggregation', 'amplitude')



By default, `mean_primitive` will be given the tag `mean`. To observe or change this tag, call the `get_tag` and `set_tag` methods, respectively.


```python
#Re-initialize mean_primitive
mean_primitive = Mean()

# Observe the current tag
print('Old tag: ', mean_primitive.get_tag())

# Re-tag mean_primitive with a custom string
mean_primitive.set_tag('mean_tag')

# Observe the new tag
print('New tag: ', mean_primitive.get_tag())

# Set the tag of mean_primitive back to mean
mean_primitive = mean_primitive.set_tag('mean')

# Observe the new tag
print('Last tag: ', mean_primitive.get_tag())
```

    Old tag:  mean
    New tag:  mean_tag
    Last tag:  mean


Tagging primitives will be useful when building pipelines.

### Primitives with hyperparameters

In our previous example, the `Mean` primitive did not offer any hyperparameters to set by the user. Let's consider the `FrequencyBand` primitive, which accepts two hyperparameters as input arguments: `low` and `high`.

To initialize the primitive, we pass in the `low` and `high` values as (keyword) arguments.


```python
# Import primitive
from sigpro.basic_primitives import FrequencyBand

# Initialize the primitive object
fb_primitive = FrequencyBand(low = 10, high = 20)

fb_primitive
```




    <sigpro.basic_primitives.FrequencyBand at 0x7f91e1a79b20>



We can preview the hyperparameters with the `get_hyperparam_dict` method.


```python
fb_primitive.get_hyperparam_dict()
```




    {'name': 'frequency_band',
     'primitive': 'sigpro.transformations.frequency.band.frequency_band',
     'init_params': {'low': 10, 'high': 20}}



### Primitive JSON Annotations

Each SigPro `Primitive` is accompanied by a corresponding JSON annotation. To preview the JSON annotation, we use the `make_primitive_json` method.


```python
import json

# More readable output
print(json.dumps(fb_primitive.make_primitive_json(), indent = 2))
```

    {
      "name": "sigpro.transformations.frequency.band.frequency_band",
      "primitive": "sigpro.transformations.frequency.band.frequency_band",
      "classifiers": {
        "type": "transformation",
        "subtype": "frequency"
      },
      "produce": {
        "args": [
          {
            "name": "amplitude_values",
            "type": "numpy.ndarray"
          },
          {
            "name": "frequency_values",
            "type": "numpy.ndarray"
          }
        ],
        "output": [
          {
            "name": "amplitude_values",
            "type": "numpy.ndarray"
          },
          {
            "name": "frequency_values",
            "type": "numpy.ndarray"
          }
        ]
      },
      "hyperparameters": {
        "fixed": {
          "low": {
            "type": "int"
          },
          "high": {
            "type": "int"
          }
        },
        "tunable": {}
      }
    }


### Primitive Interface

We summarize the public interface of the `sigpro.primitive.Primitive` class below.

| Method name | Additional arguments | Description |
| --- | --- | --- |
| `get_name` |  | Return the name of the primitive. |
| `get_tag` |  | Return the user-given tag of the primitive. |
| `get_inputs` |  | Return the inputs of the primitive. |
| `get_outputs` |  | Return the outputs of the primitive. |
| `get_type_subtype` |  | Return the type and subtype of the primitive. |
| `get_hyperparam_dict` |  | Return the hyperparameters of the primitive. |
| `get_context_arguments` |  | Return the context arguments of the primitive. |
| `get_fixed_hyperparameters` |  | Return the fixed hyperparameters of the primitive. |
| `get_tunable_hyperparameters` |  | Return the tunable hyperparameters of the primitive. |
| `set_tag` | `tag` | Set the tag of the primitive and return the primitive itself. |
| `set_context_arguments`  | `context_arguments` | Set the context arguments of the primitive to args. |
| `set_fixed_hyperparameters`  | `fixed_hyperparameters` | Set the fixed hyperparameters of the primitive. |
| `set_tunable_hyperparameters (params)` | `tunable_hyperparameters` | Set the tunable hyperparameters of the primitive. |
| `make_primitive_json` |  | Return the JSON representation of the primitive. |
| `write_primitive_json` | `primitives_path`, `primitives_subfolders` | Write the JSON representation of the primitive to the given path.  |

## Custom Primitives

In certain cases, we may be interested in writing a custom primitive class to implement our own primitive function. 

Suppose that we have already written the `mean` function within the `sigpro.aggregations.amplitude.statistical` module:

```python
import numpy as np 

...

def mean(amplitude_values):
    return np.mean(amplitude_values)
    
...
```
We have two alternatives for creating a subclass of `Primitive`:

1. Call `sigpro.contributing_primitive.make_primitive_class` while passing in any necessary additional parameters.
2. Write a subclass of the appropriate `Primitive` subclass directly and call `write_primitive_json` to record the primitive JSON.

As we can see below, both approaches lead to the same primitive json annotation and functionality.


```python
# Imports

from sigpro.primitive import AmplitudeAggregation
from sigpro.contributing_primitive import get_primitive_class
```


```python
# Approach 1: create the primitive using SigPro.

mean_path = "sigpro.aggregations.amplitude.statistical.mean"
mean_outputs = [{'name': 'mean_value', 'type': 'float'}]

# Since the JSON annotation already exists in SigPro, we call get_primitive_class instead of make_primitive_class.
# This is only for the example.
MeanDynamic = get_primitive_class(mean_path, 'aggregation', 'amplitude', primitive_outputs=mean_outputs)
mean_dynamic = MeanDynamic()
```


```python
# Approach 2: write the primitive class directly.

class MeanClass(AmplitudeAggregation):
    def __init__(self):
        super().__init__("sigpro.aggregations.amplitude.statistical.mean")
        self.set_primitive_outputs([{"name": "mean_value", "type": "float" }])

mean_class = MeanClass()
```


```python
# Check that JSON annotations are equal.

print(mean_class.make_primitive_json() == mean_dynamic.make_primitive_json())
```

    True


## Pipelines

While primitives can be quite useful on their own, the true power of `SigPro` arises in
the development of a feature engineering pipeline. These are represented by the abstract `sigpro.pipeline.Pipeline` class.

In general, feature pipelines will apply a sequence of transformation primitives consecutively, followed by a single aggregation primitive, to generate a single given feature. In the simplest scenario, we have a single defined sequence of transformation primitives we would like to apply to a signal, as well as a set of aggregations to apply to the transformed signal. This can be done with a `LinearPipeline`, which we create with the `sigpro.pipeline.build_linear_pipeline` function.

### Building Linear Pipelines

Let's consider an example pipeline where we apply the `Identity` and `FFT` transformations and the `Std` and `Var` aggregations.

First, we need to import all necessary modules and define the primitives we would like to use.


```python
# Imports

from sigpro.basic_primitives import Identity, FFT, Std, Var
from sigpro.pipeline import build_linear_pipeline
```


```python
transformations = [Identity(), FFT()]
aggregations = [Std(), Var()]
```

To build a linear pipeline, simply pass in the list of transformations and aggregations.


```python
mypipeline = build_linear_pipeline(transformations, aggregations)
```

### Inspecting Pipelines

To better understand the contents of pipelines, we can call the `get_primitives` and `get_output_features` methods to obtain the list of primitives and output features, respectively, associated with the pipeline. In particular, each feature is represented as a string of primitives separated by a period `.`, representing the sequence of operations applied to the input signal, followed by the output name of the final aggregation.


```python
# Used Primitives

used_primitives = mypipeline.get_primitives()
used_primitives
```




    [<sigpro.basic_primitives.Identity at 0x7f91b000aac0>,
     <sigpro.basic_primitives.FFT at 0x7f91e1a9d400>,
     <sigpro.basic_primitives.Std at 0x7f91b000a880>,
     <sigpro.basic_primitives.Var at 0x7f91b000aa90>]




```python
#Output features

output_features = mypipeline.get_output_features()
output_features
```




    ['identity.fft.std.std_value', 'identity.fft.var.var_value']



### More Complex Pipelines

In certain cases, we may wish to build more complex pipeline architectures. Such architectures are represented with the `LayerPipeline` subclass.

`SigPro` provides the `build_tree_pipeline(transformation_layers, aggregation_layer)` method to build tree-shaped pipelines, which generate all features in the Cartesian product of the transformation layers and aggregation layer; in other words, any possible sequence of transformations and aggregation chosen one from each layer is represented in the final feature output.


```python
# Import packages
from sigpro.basic_primitives import (
    Identity, FFT, FFTReal, Mean, Kurtosis)
from sigpro.pipeline import build_tree_pipeline

# Define primitive objects
identity_tfm = Identity().set_tag('id1') #
identity2_tfm = Identity().set_tag('id2') #Avoid duplicate tags
fft_tfm, fft_real_tfm = FFT(), FFTReal()
mean_agg, kurtosis_agg = Mean(), Kurtosis(bias=False)

# Instantiate tree pipeline
tfmlayer1 = [identity_tfm, identity2_tfm]
tfmlayer2 = [fft_tfm, fft_real_tfm]
agglayer = [mean_agg, kurtosis_agg]
tree_pipeline = build_tree_pipeline([tfmlayer1, tfmlayer2], agglayer)
```


```python
tree_pipeline.get_primitives()
```




    [<sigpro.basic_primitives.FFTReal at 0x7f91e1afd640>,
     <sigpro.basic_primitives.Identity at 0x7f91e1afde50>,
     <sigpro.basic_primitives.Mean at 0x7f91e1afde80>,
     <sigpro.basic_primitives.Kurtosis at 0x7f91e1afd6a0>,
     <sigpro.basic_primitives.Identity at 0x7f91e1afdeb0>,
     <sigpro.basic_primitives.FFT at 0x7f91e1afdb20>]




```python
tree_pipeline.get_output_features()
```




    ['id1.fft.mean.mean_value',
     'id1.fft.kurtosis.kurtosis_value',
     'id1.fft_real.mean.mean_value',
     'id1.fft_real.kurtosis.kurtosis_value',
     'id2.fft.mean.mean_value',
     'id2.fft.kurtosis.kurtosis_value',
     'id2.fft_real.mean.mean_value',
     'id2.fft_real.kurtosis.kurtosis_value']



`SigPro` allows for the generation of any arbitrary list of feature combination tuples with the `build_layer_pipeline(primitives, primitive_combinations)` method.


```python
from sigpro.basic_primitives import (
    BandMean, Identity, FFT, FFTReal, Mean, Kurtosis)
from sigpro.pipeline import build_layer_pipeline


p1, p2 = FFTReal().set_tag('fftr'), FFT()
p3, p4 = Identity().set_tag('id1'), Identity().set_tag('id2')
p5, p6, p7 = BandMean(200, 50000).set_tag('bm'), Mean(), Kurtosis(fisher=False)
p8 = Identity().set_tag('id3')  # unused primitive

all_primitives = [p1, p2, p3, p4, p5, p6, p7, p8]

features = [(p1, p3, p5), (p1, p3, p6), (p2, p3, p6), (p2, p4, p6), (p2, p4, p7)]

layer_pipeline = build_layer_pipeline(all_primitives, features)
```


```python
layer_pipeline.get_primitives()
```




    [<sigpro.basic_primitives.FFTReal at 0x7f91e1b17b80>,
     <sigpro.basic_primitives.FFT at 0x7f91e1b17760>,
     <sigpro.basic_primitives.Identity at 0x7f91e1b17040>,
     <sigpro.basic_primitives.Identity at 0x7f91e1b17550>,
     <sigpro.basic_primitives.BandMean at 0x7f91e1b33760>,
     <sigpro.basic_primitives.Mean at 0x7f91e1b33700>,
     <sigpro.basic_primitives.Kurtosis at 0x7f91e1b32400>,
     <sigpro.basic_primitives.Identity at 0x7f91e1b33730>]




```python
layer_pipeline.get_output_features()
```




    ['fftr.id1.bm.value',
     'fftr.id1.mean.mean_value',
     'fft.id1.mean.mean_value',
     'fft.id2.mean.mean_value',
     'fft.id2.kurtosis.kurtosis_value']



### Combining pipelines

If we do not wish to specify the exact combination of features to produce a `LayerPipeline`, we can still customize our feature engineering using the `sigpro.pipeline.merge_pipelines` function. By passing in a list of pipelines, we can generate a single pipeline to generate all features produced by at least one feature input.

For our example, we first initialize several primitive objects:


```python
# Import
from sigpro.pipeline import merge_pipelines

# Initialize some primitives
p1, p2 = FFTReal().set_tag('fftr'), FFT()
p3, p4 = Identity().set_tag('id1'), Identity().set_tag('id2')
p5, p6, p7 = BandMean(200, 50000).set_tag('bm'), Mean(), Kurtosis(fisher=False)
p8 = Identity().set_tag('id3')  # unused primitive
```

We next initialize three separate pipelines using the specified primitives and merge them into a single pipeline.


```python
all_primitives = [p1, p2, p3, p4, p5, p6, p7, p8]

layer_combinations = [(p1, p3, p5), (p1, p3, p6), (p2, p3, p6), (p2, p4, p6), (p2, p4, p7)]

sub_pipeline1 = build_layer_pipeline(all_primitives, layer_combinations)
sub_pipeline2 = build_tree_pipeline([[p1, p2], [p3]], [p5])
sub_pipeline3 = build_linear_pipeline([p1, p4], [p6])

merged_pipeline = merge_pipelines([sub_pipeline1, 
                                   sub_pipeline2,
                                   sub_pipeline3])
```

Lastly, we check that the merged pipeline indeed generates the union of all of the features of the sub-pipelines.


```python
expected_features = set(sub_pipeline1.get_output_features() + 
                        sub_pipeline2.get_output_features() + 
                        sub_pipeline3.get_output_features())
actual_features = set(merged_pipeline.get_output_features())

print(expected_features == actual_features)
```

    True


## Applying a Pipeline with `process_signal`

Once our pipeline is correctly defined, we apply the `process_signal` method to a demo dataset. Recall that `process_signal` is defined as follows:


```python
def process_signal(self, data=None, window=None, values_column_name='values',
                       time_index=None, groupby_index=None, feature_columns=None,
                       keep_columns=False, input_is_dataframe=True, **kwargs):
    

		...
		return data, feature_columns
```

`process_signal` accepts as input the following arguments:

- `data (pd.Dataframe)` : Dataframe with a column containing signal values.
- `window (str)`: Duration of window size, e.g. ('1h').
- `vaues_column_name (str)`: Name of the column in `data` containing signal values.
- `time_index (str)`: Name of column in `data` that represents the time index.
- `groupby_index (str or list[str])`: List of column names to group together and take the window over.
- `feature_columns (list)`: List of columns from the input data that should be considered as features (and not dropped).
- `keep_columns (bool or list[str])`:  Whether to keep non-feature columns in the output DataFrame or not. If a list of column names are passed, those columns are kept.
- `input_is_dataframe (bool)`: Whether the input data is a Dataframe. Used for MLBlocks integration.

`process_signal` outputs the following:

- `data (pd.Dataframe)`: Dataframe containing output feature values as constructed from the signal
- `feature_columns (list)`: list of (generated) feature names.

We now apply our first pipeline `mypipeline` to a toy dataset in the `xvalues`, `yvalues` format. We will define our toy dataset as follows. 


```python
# Redefine mypipeline

transformations = [Identity(), FFT()]
aggregations = [Std(), Var()]

mypipeline = build_linear_pipeline(transformations, aggregations)
```


```python
from sigpro.demo import get_demo_data
```


```python
demo_dataset = get_demo_data()
demo_dataset['xvalues'] = demo_dataset['timestamp'].copy()
demo_dataset['yvalues'] = demo_dataset['values'].copy()
demo_dataset = (demo_dataset.set_index('timestamp').resample(rule = '60T').apply(lambda x: x.to_list())).reset_index()
demo_dataset[['turbine_id', 'signal_id', 'sampling_frequency']] = demo_dataset[['turbine_id', 'signal_id', 'sampling_frequency']].apply(lambda x: x[0])
demo_dataset = demo_dataset[['turbine_id', 'signal_id', 'xvalues', 'yvalues', 'sampling_frequency']]
demo_dataset.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <td>[2020-01-01 00:00:00, 2020-01-01 00:00:01, 202...</td>
      <td>[0.43616983763682876, -0.17662312586241055, 0....</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>[2020-01-01 01:00:00, 2020-01-01 01:00:01, 202...</td>
      <td>[0.8023828754411122, -0.14122063493312714, -0....</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>[2020-01-01 02:00:00, 2020-01-01 02:00:01, 202...</td>
      <td>[-1.3143142430046044, -1.1055740033788437, -0....</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>[2020-01-01 03:00:00, 2020-01-01 03:00:01, 202...</td>
      <td>[-0.45981995520032104, -0.3255426061995603, -0...</td>
      <td>1000.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>[2020-01-01 04:00:00, 2020-01-01 04:00:01, 202...</td>
      <td>[-0.6380405111460377, -0.11924167777027689, 0....</td>
      <td>1000.0</td>
    </tr>
  </tbody>
</table>
</div>



We now call the `process_signal` method using `mypipeline`.


```python
processed_data, feature_columns = mypipeline.process_signal(demo_dataset,
                                                                values_column_name='yvalues',
                                                                time_index = 'xvalues',
                                                                keep_columns = True )
```


```python
processed_data.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>turbine_id</th>
      <th>signal_id</th>
      <th>xvalues</th>
      <th>yvalues</th>
      <th>sampling_frequency</th>
      <th>identity.fft.std.std_value</th>
      <th>identity.fft.var.var_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>[2020-01-01 00:00:00, 2020-01-01 00:00:01, 202...</td>
      <td>[0.43616983763682876, -0.17662312586241055, 0....</td>
      <td>1000.0</td>
      <td>14.444991</td>
      <td>208.657778</td>
    </tr>
    <tr>
      <th>1</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>[2020-01-01 01:00:00, 2020-01-01 01:00:01, 202...</td>
      <td>[0.8023828754411122, -0.14122063493312714, -0....</td>
      <td>1000.0</td>
      <td>12.326223</td>
      <td>151.935764</td>
    </tr>
    <tr>
      <th>2</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>[2020-01-01 02:00:00, 2020-01-01 02:00:01, 202...</td>
      <td>[-1.3143142430046044, -1.1055740033788437, -0....</td>
      <td>1000.0</td>
      <td>12.051415</td>
      <td>145.236607</td>
    </tr>
    <tr>
      <th>3</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>[2020-01-01 03:00:00, 2020-01-01 03:00:01, 202...</td>
      <td>[-0.45981995520032104, -0.3255426061995603, -0...</td>
      <td>1000.0</td>
      <td>10.657243</td>
      <td>113.576820</td>
    </tr>
    <tr>
      <th>4</th>
      <td>T001</td>
      <td>Sensor1_signal1</td>
      <td>[2020-01-01 04:00:00, 2020-01-01 04:00:01, 202...</td>
      <td>[-0.6380405111460377, -0.11924167777027689, 0....</td>
      <td>1000.0</td>
      <td>12.640728</td>
      <td>159.787993</td>
    </tr>
  </tbody>
</table>
</div>




```python
feature_columns
```




    ['identity.fft.std.std_value', 'identity.fft.var.var_value']



Success! We have managed to apply the primitives to generate features on the input dataset.


```python

```
