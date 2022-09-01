# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Plotting backend based on Matplotlib.

"""
from .axes import (
    MatplotlibAxesProxy,
    MatplotlibAxisProxy,
    MatplotlibColorbarProxy,
    MatplotlibCursorProxy,
)
from .figure import MatplotlibFigureProxy
from .plot_1d import Matplotlib1DBarProxy, Matplotlib1DLineProxy
from .plot_2d import Matplotlib2DContourProxy, Matplotlib2DRectangularMeshProxy

__all__ = (
    "MatplotlibAxesProxy",
    "MatplotlibAxisProxy",
    "MatplotlibColorbarProxy",
    "MatplotlibCursorProxy",
    "MatplotlibFigureProxy",
    "Matplotlib1DLineProxy",
    "Matplotlib1DBarProxy",
    "Matplotlib2DRectangularMeshProxy",
    "Matplotlib2DContourProxy",
)
