# -*- coding: utf-8 -*-

"""Top-level package for SigPro."""

__author__ = """MIT Data To AI Lab"""
__email__ = 'dailabmit@gmail.com'
__version__ = '0.0.1.dev0'

import os

from mlblocks import discovery

_BASE_PATH = os.path.abspath(os.path.dirname(__file__))
MLBLOCKS_PRIMITIVES = os.path.join(_BASE_PATH, 'primitives')


def get_primitives(name=None, type=None, subtype=None):
    """Get a list of the available primitives.

    Optionally filter by primitive type: ``transformation`` or ``aggregation``.

    Args:
        primitive_type (str):
            Filter by primitive type. ``transformation`` or ``aggregation``.

    Returns:
        list:
            List of the names of the available primitives.
    """
    filters = {}
    if type:
        if type not in ('transformation', 'aggregation'):
            raise ValueError('type must be `transformation` or `aggregation`.')

        filters['classifiers.type'] = type

    if subtype:
        if subtype not in ('amplitude', 'frequency', 'frequency_time'):
            raise ValueError('type must be `amplitude`, `frequency` or `frequency_time`.')

        filters['classifiers.subtype'] = subtype

    return discovery.find_primitives(name or 'sigpro', filters)
