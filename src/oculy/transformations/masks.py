# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Routines for computing masks on data.

Note that those are expected to work on numpy arrays and xarray.DataArray.

"""
import numpy as np
from atom.api import set_default

from .node import Node


class Mask(Node):
    """Node subclass used to generate boolean mask.

    The first argument is expected to be the array to use to generate the mask.

    """

    inlineable = set_default(True)


# --- Conventional filters

# FIXME once numpy 1.21 is out can use numpy.typing for better typing (ArrayLike
# will cover xarray types)


def mask_greater(array: np.ndarray, value: float) -> np.ndarray:
    return np.greater(array, value)


def mask_greater_equal(array: np.ndarray, value: float) -> np.ndarray:
    return np.greater_equal(array, value)


def mask_less(array: np.ndarray, value: float) -> np.ndarray:
    return np.less(array, value)


def mask_less_equal(array: np.ndarray, value: float) -> np.ndarray:
    return np.less_equal(array, value)


def mask_equal(array: np.ndarray, value: float) -> np.ndarray:
    return np.equal(array, value)


def mask_simequal(array: np.ndarray, value: float, tolerance: float) -> np.ndarray:
    return np.less(np.abs(array - value), tolerance)
