# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------
"""Matplotlib proxy for 2D plots (images, contours).

"""
import numpy as np
from atom.api import Bool, Typed, Value
from matplotlib.axes import Axes
# from matplotlib.transforms import Bbox

from oculy.plotting.plots import Plot2DContourProxy, Plot2DRectangularMeshProxy


class Matplotlib2DRectangularMeshProxy(Plot2DRectangularMeshProxy):
    """Matplotlib proxy for a mesh plot.

    If the grid can be identified as regular we use imshow, otherwise we use
     pcolormesh.

    """

    def activate(self):
        super().activate()
        axes_mapping = self.element.axes_mapping
        axes = (axes_mapping["x"], axes_mapping["y"])
        if axes_mapping["x"] in ("left", "right"):
            self._invert = True
            axes = axes[::-1]

        self._mpl_axes = self.element.axes.proxy._axes[axes]
        self._display_data()

    def finalize(self):
        self._line.remove()
        super().deactivate()

    def set_data(self, data):
        if self._mesh:
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
        if len(c.shape) == 2:
            pass  # No reshaping needed

        elif len(x.shape) == 1 and len(y.shape) == 1 and \
                len(x) * len(y) == len(c):
            c = np.reshape(c, (len(x), len(y)))

        elif len(x) == len(c) and len(y) == len(c):
            # Ravel to avoid weird issue with N-D array
            x, y, c = np.ravel(x), np.ravel(y), np.ravel(c)
            shape = (len(np.unique(x)), len(np.unique(y)))
            index = np.lexsort((y, x))
            x, y, c = x[index], y[index], c[index]
            if len(c) < np.product(shape):
                to_add = np.ones(np.product(shape) - len(c))
                x = np.append(x, x[-1] * to_add)
                y = np.append(y, y[-1] * to_add)
                c = np.append(c, c[-1] * to_add)
            elif len(c) > np.product(shape):
                to_add = np.ones(shape[0] - (len(c) % shape[0]))
                x = np.append(x, x[-1] * to_add)
                y = np.append(y, y[-1] * to_add)
                c = np.append(c, c[-1] * to_add)
                shape = (shape[0], -1)
            x, y, c = (np.reshape(x, shape), np.reshape(y, shape),
                       np.reshape(c, shape))

        else:
            raise RuntimeError(
                f"Cannot reshape c {c.shape} to plot it (x: {x.shape}, "
                f"y: {y.shape}"
            )

        if use_imshow:
            self._mesh = self._mpl_axes.imshow(
                c,
                origin="lower",
                aspect="auto",
            )
        else:
            # Need matplotlib > 3.3
            self._mesh = self._mpl_axes.pcolormesh(
                x,
                y,
                c,
                shading="nearest",
                cmap=self.element.colormap,
                zorder=self.element.zorder,
            )

        if self.element.axes.colorbar:
            self.element.axes.colorbar.proxy.connect_mappable(self._mesh)

        # FIXME ugly but the automatic manner does not work.
        self._mpl_axes.set_xlim((x.min(), x.max()))
        self._mpl_axes.set_ylim((y.min(), y.max()))

        self.element.axes.figure.proxy.request_redraw()


class Matplotlib2DContourProxy(Plot2DContourProxy):
    """"""

    pass  # FIXME implement
