# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Base classes for 1D plots.

"""
from typing import Mapping

import numpy as np
from atom.api import Atom, Bool, Enum, Float, Str, Typed
from enaml.colors import ColorMember, Color

from .base import BasePlot, InvalidPlotData, mark_backend_unsupported


class Plot1DProxy(Atom):
    """Base proxy for a 1D plot, ie based on 2 inputs: x, y"""

    @mark_backend_unsupported
    def set_data(self, data: "Plot1DData"):
        pass

    @mark_backend_unsupported
    def set_axes_mapping(self, mapping: Mapping[str, str]):
        pass

    @mark_backend_unsupported
    def set_color(self, color: Color):
        pass


class Plot1DLineProxy(Plot1DProxy):
    """Base proxy for a 1D line plot.

    The same element is expected to also handle markers.

    """

    @mark_backend_unsupported
    def set_line_weigth(self, weight: int):
        pass

    @mark_backend_unsupported
    def set_marker_size(self, size: int):
        pass

    @mark_backend_unsupported
    def set_marker_shape(self, shape: str):
        pass

    @mark_backend_unsupported
    def set_marker_state(self, state: bool):
        pass


class Plot1DBarProxy(Plot1DProxy):
    """Base proxy for a 1D histogram."""

    pass


class Plot1DData(Atom):

    #: X data for the plot.
    x = Typed(np.ndarray)

    #: Y data for the plot.
    y = Typed(np.ndarray)

    #: Error bars for X data
    dx = Typed(np.ndarray)

    #: Error bars for Y data
    dy = Typed(np.ndarray)

    def __init__(self, x, y, dx=None, dy=None):
        super().__init__(x=x, y=y, dx=dx, dy=dy)
        if not x.shape == y.shape:
            raise InvalidPlotData(
                "Both x and y data of a 1D plot must have the same shape. "
                f"Got x: {x.shape}, y: {y.shape}."
            )

        # FIXME this assumes len(x.shape) == 1

        if dx and not dx.shape[0] == x.shape[0]:
            raise InvalidPlotData(
                "Both x and dx data of a 1D plot must have the same number of "
                "points (ie first dimension). "
                f"Got x: {x.shape}, dx: {dx.shape}."
            )

        if dy and not dy.shape[0] == y.shape[0]:
            raise InvalidPlotData(
                "Both y and dy data of a 1D plotmust have the same number of "
                "points (ie first dimension). "
                f"Got y: {y.shape}, dx: {dy.shape}."
            )

        # Make the object unmutable.
        self.freeze()


class Plot1D(BasePlot):
    """"""

    #: Data for the plot
    data = Typed(Plot1DData).tag(sync=True)

    # --- Proxy connection

    def _post_setattr_data(self, old, new):
        if self.proxy:
            self.proxy.set_data(new)


class Plot1DLine(Plot1D):
    """"""

    #: Color of the plot
    color = ColorMember()

    #: Weight of the line
    line_weight = Float(1.0)

    #: Style of the line
    line_style = Str()

    #: Should markers be displayed
    markers_enabled = Bool()

    #: Size of the markers
    markers_size = Float()

    #: Shape of the marker
    # FIXME complete
    marker_shape = Enum(
        (
            "*",
            "+",
        )
    )

    # FIXME add connection to proxy


class Plot1DBar(Plot1D):
    """"""

    pass
