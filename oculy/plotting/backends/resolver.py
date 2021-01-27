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

from atom.api import Atom, Callable, Dict, Typed, Str
from enaml.workbench.api import Workbench

from ..plots import BasePlot, Axes

T = TypeVar("T", bound=BasePlot)


class PlotResolver(Atom):
    """Base plot resolver."""

    #: Instance of the application workbench.
    workbench = Typed(Workbench)

    #: Name of the backend for this resolver instance is used with
    backend_name = Str()

    #: Backend specific handlers that can be used to add a plot to a set of axes.
    plot_handlers = Dict(BasePlot, Callable)

    def add_plot(self, axes: Axes, plot: T, plot_axes: Mapping[str, str]) -> T:
        """Add a plot to a set of axes.

        Parameters
        ----------
        axes: Axes
            Axes in which to add the plot.

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
        plot_type = type(plot)

        if plot_type not in self.plot_handlers:
            raise RuntimeError(
                f"Plot type {plot_type} is not supported by {self.backend_name}"
            )

        # Validate the axes supposed to be used.
        if plot_axes and any(
            (pa not in axes.axes or axes.axes[pa] is None) for pa in plot_axes.values()
        ):
            unknown = []
            missing = []
            for lab, pa in plot_axes.items():
                if pa not in axes.axes:
                    unknown.append((lab, pa))
                elif axes.axes[pa] is None:
                    missing.append((lab, pa))
            if missing:
                raise RuntimeError(
                    f"The axes used for {[lab for lab, _ in unknown]} do not "
                    "correspond to any valid axes (valid axes are "
                    "'left', 'right', 'top', 'bottom', provided axes are "
                    f"{[pa for _, pa in unknown]})."
                )
            else:
                raise RuntimeError(
                    f"The axes used for {[lab for lab, _ in missing]} do not "
                    "exist. Existing axes are "
                    f"{[ax for ax in axes.axes._fields if axes.axes[ax] is not None]}, "
                    f"specified axes are {[pa for _, pa in missing]}."
                )

        return self.plot_handlers[plot_type](axes, plot, plot_axes)
