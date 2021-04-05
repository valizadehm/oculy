# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Matplotlib proxy for 2D plots (images, contours).

"""
import numpy as np
from atom.api import Bool, Typed, Value
from matplotlib.axes import Axes

from oculy.plotting.plots import Plot2DContourProxy, Plot2DRectangularMeshProxy


class Matplotlib2DRectangularMeshProxy(Plot2DRectangularMeshProxy):
    """Matplotlib proxy for a mesh plot.

    If the grid can be identified as regular we use imshow, otherwise we use pcolormesh.

    """

    def activate(self):
        super().activate()
        axes_mapping = self.element.axes_mapping
        axes = (axes_mapping["x"], axes_mapping["y"])
        if axes_mapping["x"] in ("left", "right"):
            self._invert = True
            axes = axes[::-1]

        self._mpl_axes = self.element.axes._proxy._axes[axes]
        self._display_data()

    def finalize(self):
        self._line.remove()
        super().deactivate()

    def set_data(self, data):
        self._mesh.remove()
        self._display_data()

    # --- Private API

    #: Matplotlib axes in which to draw
    _mpl_axes = Typed(Axes)

    #: Do we need to invert and y due to the axes mapping
    _invert = Bool()

    #: Reference to the currently displayed mesh
    _mesh = Value()

    def _display_data(self):
        data = self.element.data
        use_imshow = False
        x, y, c = data.x, data.y, data.c
        if self._invert:
            x, y = y, x
        if len(x.shape) == 2:
            if len(np.unique(data.x[0])) == 1 and len(np.unique(data.y[:, 0])) == 1:
                # FIXME use imshow
                pass
            elif len(np.unique(data.x[:, 0])) == 1 and len(np.unique(data.y[0])) == 1:
                # FIXME use imshow
                pass

        else:
            # Ravel to avoid weird issue with N-D array
            x, y, c = np.ravel(data.x), np.ravel(data.y), np.ravel(data.c)
            if x[0] == x[1]:
                # FIXME Keep going to find the redundance and check for possibility to use imshow
                pass
            elif y[0] == y[1]:
                # FIXME Keep going to find the redundance and check for possibility to use imshow
                pass

        if use_imshow:
            pass
        else:
            # Need matplotlib > 3.3
            self._mesh = self._mpl_axes.pcolormesh(
                c,
                x,
                y,
                shading="nearest",
                cmap=self.element.colormap,
                zorder=self.element.zorder,
            )

        if self.element.axes.colorbar:
            self.element.axes.colorbar.proxy.connect_mappable(self._mesh)


class Matplotlib2DContourProxy(Plot2DContourProxy):
    """"""

    pass  # FIXME implement
