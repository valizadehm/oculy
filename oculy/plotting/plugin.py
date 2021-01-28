# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Plotting plugin logic.

"""
from typing import Mapping, Optional, Tuple

from atom.api import Atom, Dict, Typed
from enaml.workbench.api import Plugin

from .plots import Axes, BasePlot, Figure, GridPosition
from .sync_manager import SyncManager


class PlottingPlugin(Plugin):
    """Plugin handling plotting of data."""

    #: Mapping of figures managed by the plugin. Should not be edited in place.
    figures = Dict(str, Figure)

    #: Manager responsible to handle refreshing the plots linked to the data plugin.
    sync_managers = Dict(BasePlot, SyncManager)

    def create_figure(
        self,
        id: str,
        axes_positions: Optional[Mapping[str, GridPosition]] = None,
        axes_specifications: Optional[Mapping[str, Optional[Axes]]] = None,
    ) -> None:
        """Create a figure with a set of axis.

        Parameters
        ----------
        id : str
            Id of the figure which will be used to refer to it.
        axes_positions : Optional[Mapping[str, GridPosition]]
            Id of each axis and its specific position, default to None which
            will create a single axes for the figure with `default` as id.
        axes_specifications : Optional[Mapping[str, Axes]], optional
            Specification of each axes, default to None which will create
            a left and bottom axis.

        """
        if id in self.figures:
            raise KeyError(f"Figure id {id} already exists.")

        if axes_positions is None:
            axes_positions = {"default": GridPosition(0, 0)}

        if axes_specifications is None:
            axes_specifications = {}

        # XXX Validate specifications and  positions

        figure = Figure()
        for axes_id in axes_specifications:
            figure.add_axes(
                axes_id, axes_positions[axes_id], axes_specifications.get(axes_id)
            )
        self.figures[id] = figure

    def destroy_figure(self, id: str):
        """Destroy a figure."""
        if id not in self.figures:
            raise KeyError(f"Figure id {id} is not known.")
        fig = self.figures[id]
        del self.figures[id]
        fig.finalize()

    def add_plot(
        self,
        fig_id: str,
        plot_id: str,
        plot: BasePlot,
        axes_id: Optional[str] = None,
        axes: Optional[Tuple[str, str]] = None,
        sync_data: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Add a plot a to the specified figure.

        Parameters
        ----------
        fig_id : str
            Id of the figure in which to add the plot.
        plot_id : str
            Id of the plot to add.
        plot : BasePlot
            Plot to be added to the figure.
        axes_id : Optional[str], optional
            Id of the axes to which to add the plot. None by default which
            means the plot will be added to the default axes (id: "default").
        axes : Optional[Tuple[str, str]], optional
            Pair of axes to use (ex: "bottom", "left" which the default).
        sync_data : Optional[Mapping[str, str]], optional
            Mapping between attributes of the plot and entries of the data handling
            plugin.

        """
        if fig_id not in self.figures:
            raise KeyError(f"Figure id {fig_id} does not exist.")

        figure = self.figures[fig_id]
        axes_id = "default" if axes_id is None else axes_id
        if axes_id not in figure.axes_set:
            raise KeyError(
                f"Axes id {axes_id} does not exist in figure {fig_id}, "
                f"known axes are {list(figure.axes_set)}"
            )

        ax = figure.axes_set[axes_id]
        if plot_id in ax.plots:
            raise KeyError(
                f"Plot id {plot_id} already exist for axes {axes_id} of figure {fig_id}"
            )

        if sync_data:
            pass  # XXX

        ax.add_plot(plot_id, plot, axes)
