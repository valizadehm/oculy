# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Routines for computing masks on data.

"""
from typing import Any, Tuple

import numpy as np
from numba import njit


#: Description of a masking operation. Used in particular for loaders. The first
#: str should refer to the ids of a Mask contributed to the transformation plugin.
MaskSpecification = Tuple[str, Tuple[Any, ...]]


@njit
def mask_greater(array: np.ndarray, value: float) -> np.ndarray:
    return np.greater(array, value)


@njit
def mask_greater_equal(array: np.ndarray, value: float) -> np.ndarray:
    return np.greater_equal(array, value)


@njit
def mask_less(array: np.ndarray, value: float) -> np.ndarray:
    return np.less(array, value)


@njit
def mask_less_equal(array: np.ndarray, value: float) -> np.ndarray:
    return np.less_equal(array, value)


@njit
def mask_equal(array: np.ndarray, value: float) -> np.ndarray:
    return array == value


@njit
def mask_simequal(array: np.ndarray, value: float, tolerance: float) -> np.ndarray:
    return np.less(np.abs(array - value), tolerance)
