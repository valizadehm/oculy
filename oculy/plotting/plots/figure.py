# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""
"""
from .base import PlotElement, PlotElementProxy


class Cell(PlotElement):
    def add_axes(self, new_position: str, shared_position: str):
        pass

    def remove_axis(self, position: str):
        pass


class Grid(PlotElement):
    pass


class Figure(PlotElement):
    pass
