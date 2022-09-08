# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# ---------------------------------------------------------------------------
"""Base classes for 2D plots.

"""
from typing import Mapping

import numpy as np
from atom.api import Atom, Str, Typed

from .base import BasePlot, InvalidPlotData, PlotElementProxy, \
    mark_backend_unsupported


class Plot2DProxy(PlotElementProxy):
    """"""

    @mark_backend_unsupported
    def set_axes_mapping(self, mapping: Mapping[str, str]):
        pass

    @mark_backend_unsupported
    def set_data(self, data):
        pass


class Plot2DRectangularMeshProxy(Plot2DProxy):
    """"""

    pass


class Plot2DContourProxy(Plot2DProxy):
    """"""

    @mark_backend_unsupported
    def set_contour_values(self, limits):
        """"""
        pass


class Plot2DData(Atom):

    #: X data for the plot.
    x = Typed(np.ndarray)

    #: Y data for the plot.
    y = Typed(np.ndarray)

    #: C data for the plot.
    c = Typed(np.ndarray)

    def __init__(self, x, y, c):
        super().__init__(x=x, y=y, c=c)
        if not x.shape == y.shape and y.shape == c.shape:
            raise InvalidPlotData(
                "x, y and c data of a 2D plot must have the same shape. "
                f"Got x: {x.shape}, y: {y.shape}, c: {c.shape}."
            )

        # Make the object immutable.
        self.freeze()


class Plot2D(BasePlot):
    """"""

    #: Data for the plot.
    data = Typed(Plot2DData).tag(sync=True)

    #: Colormap to use.
    colormap = Str("viridis")

    # --- Proxy connection

    def _post_setattr_data(self, old, new):
        if self.proxy:
            self.proxy.set_data(new)


class Plot2DRectangularMesh(Plot2D):
    """"""

    pass


class Plot2DContour(Plot2D):
    """"""

    #: Data vault name referring to the values for which to display the
    # contour values.
    contour_values = Typed(np.ndarray).tag(sync=True)
    # FIXME add connection to proxy
