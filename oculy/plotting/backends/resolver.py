# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Base class for plot resolver in charge of handling plotting for each class of plot.

"""
from typing import TypeVar

from ..plots import BasePlot

T = TypeVar(bounds=BasePlot)


class PlotResolver(Atom):
    """Base plot resolver."""

    def add_plot(self, axes, plot: T, plot_axes) -> T:
        """Add a plot"""
        pass
