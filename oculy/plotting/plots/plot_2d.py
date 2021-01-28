# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Base classes for 2D plots.

"""
import numpy as np
from atom.api import Atom, Typed

from .base import BasePlot, mark_backend_unsupported
from ..sync_manager import ShapeMatchingMarker


# XXX Use subclass for each type (may require different option)
class Plot2DProxy(Atom):
    """"""

    @mark_backend_unsupported
    def update_data(self, x=None, y=None, c=None):
        pass


class Plot2DMeshProxy(Plot2DProxy):
    """"""

    pass


class Plot2DContourProxy(Plot2DProxy):
    """"""

    @mark_backend_unsupported
    def set_contour_values(self, limits):
        """"""
        pass


class Plot2D(BasePlot):
    """"""

    #: Name of the X data for the plot in the data vault
    x_data = Typed(np.ndarray).tag(
        sync=ShapeMatchingMarker(matching_attributes=("y_data", "c_data"))
    )

    #: Name of the Y data for the plot in the data vault
    y_data = Typed(np.ndarray).tag(
        sync=ShapeMatchingMarker(matching_attributes=("x_data", "c_data"))
    )

    #: Name of the C data for the plot in the data vault
    c_data = Typed(np.ndarray).tag(
        sync=ShapeMatchingMarker(matching_attributes=("x_data", "y_data"))
    )

    # XXX add connection to proxy


class Plot2DMesh(Plot2D):
    """"""

    pass


class Plot2DContour(Plot2D):
    """"""

    #: Data vault name referring to the values for which to display the contour values.
    contour_values = Typed(np.ndarray).tag(sync=True)
    # XXX add connection to proxy
