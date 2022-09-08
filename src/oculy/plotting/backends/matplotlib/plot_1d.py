# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# ---------------------------------------------------------------------------
"""
"""
from atom.api import Bool, Typed
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from matplotlib.lines import Line2D

from oculy.plotting.plots import Plot1DBarProxy, Plot1DLineProxy


class Matplotlib1DLineProxy(Plot1DLineProxy):
    """Matplotlib proxy handling line plot."""

    def activate(self):
        super().activate()
        axes_mapping = (
            self.element.axes_mapping or
            self.element.axes.get_default_axes_mapping()
        )
        axes = (axes_mapping["x"], axes_mapping["y"])
        data = (self.element.data.x, self.element.data.y)
        ddata = (self.element.data.dx, self.element.data.dy)
        if axes_mapping["x"] in ("left", "right"):
            self._invert = True
            axes = axes[::-1]
            data = data[::-1]
            ddata = ddata[::-1]

        mpl_axes = self.element.axes.proxy._axes[axes]
        if self.element.data.dx or self.element.data.dy:
            raise RuntimeError("Errorbars are not currently supported.")
        else:
            # FIXME handle extra states
            self._line = mpl_axes.plot(*data, zorder=self.element.zorder)[0]
        self.element.axes.figure.proxy.request_redraw()

    def deactivate(self):
        self._line.remove()
        self.element.axes.figure.proxy.request_redraw(clear=True)
        super().deactivate()

    def set_data(self, data):
        d = (data.x, data.y)
        dd = (data.dx, data.dy)
        if self._invert:
            d = d[::-1]
            dd = dd[::-1]

        # FIXME handle error bars
        self._line.set_data(*d)
        # XXX FIXME ugly hack, need a better propagation mechanism here !
        for ax in self.element.axes.proxy._axes.values():
            ax.relim()
            ax.autoscale()
        self.element.axes.figure.proxy.request_redraw()

    # --- Private API

    #: Do we need to invert x and y due to the axes mapping
    _invert = Bool()

    #: Line created by the backend.
    _line = Typed(Line2D)


class Matplotlib1DBarProxy(Plot1DBarProxy):
    """Matplotlib proxy for a 1D histogram."""

    def activate(self):
        super().activate(resolver)
        axes_mapping = self.element.axes_mapping
        axes = (axes_mapping["x"], axes_mapping["y"])
        if axes_mapping["x"] in ("left", "right"):
            self._invert = True
            axes = axes[::-1]

        self._mpl_axes = self.element.axes.proxy._axes[axes]
        self._draw_bars()
        self.element.axes.figure.proxy.request_redraw()

    def deactivate(self):
        self._bar.remove()
        self.element.axes.figure.proxy.request_redraw(clear=True)

    def set_data(self, data):
        self._bar.remove()
        self._draw_bars()
        # FIXME ugly hack, need a better propagation mechanism here !
        for ax in self.element.axes.proxy._axes.values():
            ax.relim()
            ax.autoscale()
        self.element.axes.figure.proxy.request_redraw()

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
