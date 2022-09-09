# -------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# ---------------------------------------------------------------------------
""" Objects used to represent plots in a backend independent manner.

"""
from .axes import (
    Axes,
    AxesProxy,
    Axis,
    AxisProxy,
    Colorbar,
    ColorbarProxy,
    Cursor,
    CursorProxy,
)
from .base import BasePlot, BasePlotProxy, Plot
from .figure import Figure, FigureProxy, GridPosition
from .plot_1d import Plot1DBar, Plot1DBarProxy, Plot1DData, Plot1DLine, Plot1DLineProxy
from .plot_2d import (
    Plot2DContour,
    Plot2DContourProxy,
    Plot2DData,
    Plot2DRectangularMesh,
    Plot2DRectangularMeshProxy,
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
    "GridPosition",
    "Plot1DData",
    "Plot1DLine",
    "Plot1DBar",
    "Plot1DLineProxy",
    "Plot1DBarProxy",
    "Plot2DData",
    "Plot2DRectangularMesh",
    "Plot2DContour",
    "Plot2DRectangularMeshProxy",
    "Plot2DContourProxy",
)
