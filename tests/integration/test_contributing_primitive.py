"""Test module for SigPro contributing_primitive module."""

import json
import os
import tempfile

from sigpro.basic_primitives import Mean
from sigpro.contributing_primitive import make_primitive_class

EXPECTED_PRIMITIVE_DICT = {
    "name": "sigpro.aggregations.amplitude.statistical.mean",
    "primitive": "sigpro.aggregations.amplitude.statistical.mean",
    "classifiers": {
        "type": "aggregation",
        "subtype": "amplitude"
    },
    "produce": {
        "args": [
            {
                "name": "amplitude_values",
                "type": "numpy.ndarray"
            }
        ],
        "output": [
            {
                "name": "mean_value",
                "type": "float"
            }
        ]
    },
    'hyperparameters': {
        'fixed': {},
        'tunable': {}
    }
}


def test_make_primitive_class_primitives_subfolders_true():
    with tempfile.TemporaryDirectory('sigpro') as tmp_dir:
        expected_result = ['sigpro', 'aggregations', 'amplitude', 'statistical', 'mean.json']
        expected_result = os.path.join(tmp_dir, *expected_result)
        primitive_outputs = [{'name': 'mean_value', 'type': 'float'}]
        Mean_dynamic, result = make_primitive_class(
            'sigpro.aggregations.amplitude.statistical.mean',
            'aggregation',
            'amplitude',
            primitives_path=tmp_dir,
            primitive_outputs=primitive_outputs
        )
        assert result == expected_result
        with open(result, 'rb') as created_primitive:
            primitive_dict = json.load(created_primitive)
            assert primitive_dict == EXPECTED_PRIMITIVE_DICT

        mean_instance = Mean_dynamic()
        mean_default = Mean()
        assert mean_instance.make_primitive_json() == mean_default.make_primitive_json()


def test_make_primitive_class_primitives_subfolders_false():
    with tempfile.TemporaryDirectory('sigpro') as tmp_dir:
        expected_result = 'sigpro.aggregations.amplitude.statistical.mean.json'
        expected_result = os.path.join(tmp_dir, expected_result)
        primitive_outputs = [{'name': 'mean_value', 'type': 'float'}]
        Mean_dynamic, result = make_primitive_class(
            'sigpro.aggregations.amplitude.statistical.mean',
            'aggregation',
            'amplitude',
            primitives_path=tmp_dir,
            primitive_outputs=primitive_outputs,
            primitives_subfolders=False
        )
        assert result == expected_result
        with open(result, 'rb') as created_primitive:
            primitive_dict = json.load(created_primitive)
            assert primitive_dict == EXPECTED_PRIMITIVE_DICT

        mean_instance = Mean_dynamic()
        mean_default = Mean()
        assert mean_instance.make_primitive_json() == mean_default.make_primitive_json()
