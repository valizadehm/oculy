# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Base classes for 2D plots.

"""
from typing import Any, Optional, Sequence, Tuple, Mapping

import numpy as np
from atom.api import Atom, Typed

from .base import BasePlot, mark_backend_unsupported


# XXX Use subclass for each type (may require different option)
class Proxy2DPlot(Atom):
    """"""

    @mark_backend_unsupported
    def update_data(self, x=None, y=None, c=None):
        pass


class Proxy2DMeshPlot(Proxy2DPlot):
    """"""

    pass


class Proxy2DContourPlot(Proxy2DPlot):
    """"""

    @mark_backend_unsupported
    def set_contour_values(self, limits):
        """"""
        pass


class Plot2D(BasePlot):
    """"""

    #: X data for the plot
    x_data = Typed(np.ndarray)

    #: Y data for the plot
    y_data = Typed(np.ndarray)

    #: C data for the plot
    c_data = Typed(np.ndarray)

    # XXX add connection to proxy


class Plot2DMesh(Plot2D):
    """"""

    pass


class Plot2DContour(Plot2D):
    """"""

    #: Specific values for which diplay the contour values.
    contour_values = Typed(np.ndarray)

    # XXX add connection to proxy
