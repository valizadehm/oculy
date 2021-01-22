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
class Proxy2DPlot(Atom):
    """"""

    def update_data(self, x=None, y=None):
        pass


class Proxy2DMeshPlot(Proxy2DPlot):
    """"""

    def set_color_limits(self, limits):
        """"""
        pass


class Proxy2DContourPlot(Proxy2DPlot):
    """"""

    def set_contour_values(self, limits):
        """"""
        pass


class Plot2D(BasePlot):
    """"""

    pass


class Plot2DMesh(Plot2D):
    """"""

    pass


class Plot2DContour(Plot2D):
    """"""

    pass
