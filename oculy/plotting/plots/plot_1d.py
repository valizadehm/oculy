# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""
"""
from typing import Any, Optional, Sequence, Tuple, Mapping

from atom.api import Atom

from . import BasePlot

# WIP on API


# XXX Use subclass for each type (may require different option)
class Proxy1DPlot(Atom):
    """"""

    def update_data(self, x=None, y=None):
        pass

    def set_color(self, color):
        pass


class Proxy1DLinePlot(Proxy1DPlot):
    def set_line_weigth(self, weight: int):
        pass

    def set_marker_size(self, size: int):
        pass

    def set_marker_state(self, state: bool):
        pass


class Proxy1DHistogramPlot(Proxy1DPlot):
    pass


class Plot1D(BasePlot):
    """"""

    pass


class Plot1DLine(Plot1D):
    """"""

    pass


class Plot1DHistogram(Plot1D):
    """"""

    pass
