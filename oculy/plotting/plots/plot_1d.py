# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""
"""
from typing import Any, Sequence, Mapping

from atom.api import Atom

# WIP on API


class Proxy1DAxis(Atom):
    """ """

    def set_x_axis_scale(self, scale):
        pass

    def set_y_axis_scale(self, scale):
        pass

    def set_x_autoscaling(self, setting: bool):
        pass

    def set_y_autoscaling(self, setting: bool):
        pass

    def enable_zooming(self, bound: str, button: str):
        pass

    def disable_zooming(self):
        pass

    def enable_panning(self, button: str):
        pass

    def disable_panning(self):
        pass

    def add_cursor(self):
        pass

    def remove_cursor(self):
        pass

    def enable_grid(self):
        pass

    def set_xlabel(self, title: str, font: Mapping[str, Any]):
        pass

    def set_ylabel(self, title: str, font: Mapping[str, Any]):
        pass

    def set_xtick_labels(self, labels: Sequence[str], font: Mapping[str, Any]):
        pass

    def set_ytick_labels(self, labels: Sequence[str], font: Mapping[str, Any]):
        pass

    def set_legend(self, legend: Mapping[str, str]):
        pass

    def set_plot_type(self, id: str, plt_type: str):  # (line, line + marker, histo)
        pass

    def add_plot(self, id, x, y):
        pass

    def remove_plot(self, id):
        pass


# XXX Use subclass for each type (may require different option)
class Proxy1DPlot(Atom):
    def update_data(self, x=None, y=None):
        pass

    def set_color(self, color):
        pass

    def set_size(self, size: int):
        pass
