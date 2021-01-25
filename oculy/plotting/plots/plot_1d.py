# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Base classes for 1D plots.

"""
from typing import Any, Optional, Sequence, Tuple, Mapping

import numpy as np
from atom.api import Atom, Bool, Float, Typed
from enaml.colors import ColorMember

from .base import BasePlot, mark_backend_unsupported

# WIP on API


# XXX Use subclass for each type (may require different option)
class Proxy1DPlot(Atom):
    """"""

    @mark_backend_unsupported
    def update_data(self, x=None, y=None):
        pass

    @mark_backend_unsupported
    def set_color(self, color):
        pass


class Proxy1DLinePlot(Proxy1DPlot):
    @mark_backend_unsupported
    def set_line_weigth(self, weight: int):
        pass

    @mark_backend_unsupported
    def set_marker_size(self, size: int):
        pass

    @mark_backend_unsupported
    def set_marker_state(self, state: bool):
        pass


class Proxy1DHistogramPlot(Proxy1DPlot):
    pass


class Plot1D(BasePlot):
    """"""

    #: X data for the plot
    x_data = Typed(np.ndarray)

    #: Y data for the plot
    y_data = Typed(np.ndarray)

    # XXX add connection to proxy


class Plot1DLine(Plot1D):
    """"""

    #: Color of the plot
    color = ColorMember()

    #: Weight of the line
    line_weight = Float()

    #: Should markers be displayed
    markers_enabled = Bool()

    #: Size of the markers
    markers_size = Float()

    # XXX add connection to proxy


class Plot1DHistogram(Plot1D):
    """"""

    pass
