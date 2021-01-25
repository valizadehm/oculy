# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""
"""
from atom.api import Atom, Int, Dict

from .base import PlotElement, PlotElementProxy
from .axes import Axes


class FigureProxy(PlotElementProxy):
    """Proxy for a figure."""

    pass


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

    def add_axes(self, id: str, position: GridPosition) -> Axes:
        """"""
        pass

    def remove_axes(self, id: str):
        """"""
        pass
