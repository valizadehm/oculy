# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Base class for plot resolver in charge of handling plotting for each class of plot.

"""
from typing import TypeVar, Mapping

from atom.api import Atom, Callable, Dict, Typed
from enaml.workbench.api import Workbench

from ..plots import BasePlot, Axes

T = TypeVar("T", bound=BasePlot)


class PlotResolver(Atom):
    """Base plot resolver."""

    #: Instance of the application workbench.
    workbench = Typed(Workbench)

    #: Backend specific handlers that can be used to add a plot to a set of axes.
    plot_handlers = Dict(BasePlot, Callable)

    def add_plot(self, axes: Axes, plot: T, plot_axes: Mapping[str, str]) -> T:
        """Add a plot to a set of axes.

        Parameters
        ----------
        axes: Axes
            Axes in which to add teh plot.

        plot: BasePlot
            Description class of the plot to add. The proxy will be populated by
            the specific handler that will be called.

        plot_axes: Mapping[str, str]
            Mapping between the axes "x", "y" (and "c" for 2D plots) and
            "left", "bottom", "top", "right" axes that can exist in the provided
            axes object.

        Returns
        -------
        BasePlot:
            Description class of the plot to add whose ``proxy`` and ``data_vault``
            fields have been populated.

        """
        # Write the logic dispatching to the backend
        pass
