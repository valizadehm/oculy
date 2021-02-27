# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""
"""
from atom.api import Bool, Typed
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.lines import Lines2D

from ..plots import Plot1DBarProxy, Plot1DLineProxy


class Matplotlib1DLineProxy(Plot1DLineProxy):
    """Matplotlib proxy handling line plot."""

    def initialize(self, resolver):
        super().initialize(resolver)
        axes_mapping = self.element.axes_mapping
        axes = (axes_mapping["x"], axes_mapping["y"])
        data = (self.element.data.x, self.element.data.y)
        ddata = (self.element.data.dx, self.element.data.dy)
        if axes_mapping["x"] in ("left", "right"):
            self._invert = True
            axes = axes[::-1]
            data = data[::-1]
            ddata = ddata[::-1]

        mpl_axes = self.element.axes._proxy._axes[axes]
        if self.element.data.dx or self.element.data.dy:
            raise RuntimeError("Errorbars are not currently supported.")
        else:
            # FIXME handle extra states
            self._line = mpl_axes.plot(*data, zorder=self.element.zorder)[0]

    def finalize(self):
        self._line.remove()

    def set_data(self, data):
        data = (data.x, data.y)
        ddata = (data.dx, data.dy)
        if self._invert:
            data = data[::-1]
            ddata = ddata[::-1]

        # FIXME handle error bars
        self._line.set_data(*data)

    # --- Private API

    #: Do we need to invert and y due to the axes mapping
    _invert = Bool()

    #: Line created by the backend.
    _line = Typed(Lines2D)


class Matplotlib1DBarProxy(Plot1DBarProxy):
    """Matplotlib proxy for a 1D histogram."""

    def initialize(self, resolver):
        super().initialize(resolver)
        axes_mapping = self.element.axes_mapping
        axes = (axes_mapping["x"], axes_mapping["y"])
        if axes_mapping["x"] in ("left", "right"):
            self._invert = True
            axes = axes[::-1]

        self._mpl_axes = self.element.axes._proxy._axes[axes]
        self._draw_bars()

    def finalize(self):
        self._bar.remove()

    def set_data(self, data):
        self._bar.remove()
        self._draw_bars()

    # --- Private API

    #: Do we need to invert and y due to the axes mapping
    _invert = Bool()

    #: Line created by the backend.
    _bar = Typed(BarContainer)

    #: Matplotlib axes in which to draw the bars
    _mpl_axes = Typed(Axes)

    def _draw_bars(self):
        data = (self.element.data.x, self.element.data.y)
        if self._invert:
            data = data[::-1]

        self._bar = self._mpl_axes.bar(
            *data, width=data[0][1] - data[0][0], zorder=self.element.zorder
        )
