# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
""" Objects used to represent plots in a backend independent manner.

"""
from .axes import (
    Axes,
    Axis,
    Colorbar,
    Cursor,
    AxesProxy,
    AxisProxy,
    ColorbarProxy,
    CursorProxy,
)
from .base import BasePlot, BasePlotProxy, Plot
from .figure import Figure, FigureProxy
from .plot_1d import Plot1DLine, Plot1DHistogram, Plot1DLineProxy, Plot1DHistogramProxy
from .plot_2d import (
    Plot2DMesh,
    Plot2DContour,
    Plot2DMeshProxy,
    Plot2DContourProxy,
)

__all__ = (
    "Axes",
    "Axis",
    "Colorbar",
    "Cursor",
    "AxesProxy",
    "AxisProxy",
    "ColorbarProxy",
    "CursorProxy",
    "BasePlot",
    "BasePlotProxy",
    "Plot",
    "Figure",
    "FigureProxy",
    "Plot1DLine",
    "Plot1DHistogram",
    "Plot1DLineProxy",
    "Plot1DHistogramProxy",
    "Plot2DMesh",
    "Plot2DContour",
    "Plot2DMesh",
    "Plot2DMeshProxy",
    "Plot2DContourProxy",
)
