# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""
"""
from typing import Optional
from atom.api import Atom, Int, Dict, Typed

from .base import PlotElement, PlotElementProxy
from .axes import Axes
from ..backends.resolver import BackendResolver


class FigureProxy(PlotElementProxy):
    """Proxy for a figure."""

    def get_native_widget(self, parent):
        """"""
        raise NotImplementedError()


class GridPosition(Atom):
    """Position of axes in the figure grid."""

    #: Index of the bottom position for the axes (inclusive)
    bottom = Int()

    #: Index of the top position for the axes (exclusive)
    top = Int()

    #: Index of the left position for the axes (inclusive)
    left = Int()

    #: Index of the right position for the axes (exclusive)
    right = Int()

    def __init__(self, left, bottom, right=None, top=None) -> None:
        right = right or left + 1
        top = top or bottom + 1
        super().__init__(left=left, right=right, bottom=bottom, top=top)


class Figure(PlotElement):
    """Figure holding possibly multiple axes on a grid."""

    #: Set of axes on a grid.
    axes_set = Dict(str, Axes)

    #: Position of the axes on the grid
    grid = Dict(str, GridPosition)

    def initialize(self, resolver):
        """Initialize the proxy of the figure and the axes."""
        self._resolver = resolver
        super().initialize(resolver)
        for axes in self.axes_set.values():
            axes.figure = self
            axes.backend_name = self.backend_name
            axes.initialize(resolver)

    def finalize(self):
        """Finalize the proxy of the figure."""
        for axes in self.axes_set.values():
            axes.figure = self
            axes.finalize()
        super().finalize()

    def add_axes(
        self, id: str, position: GridPosition, axes: Optional[Axes] = None
    ) -> Axes:
        """Add an axes to the figure"""
        axes = axes or Axes()
        self.axes_set[id] = axes
        self.grid[id] = position
        if self.proxy and self.proxy.is_active:
            axes.activate()

        return axes

    def remove_axes(self, id: str):
        """"""
        pass  # FIXME not needed as long as we have a single axes per figure

    # --- Private API

    #: Reference to the backend resolver needed to dynamically add axes
    _resolver = Typed(BackendResolver)
