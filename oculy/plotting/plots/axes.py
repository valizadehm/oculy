# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""
"""
from typing import Any, Optional, Sequence, Tuple, Mapping, NamedTuple

from atom.api import (
    Atom,
    Str,
    Typed,
    Bool,
    List,
    Dict,
    Float,
    Tuple as ATuple,
    Callable,
)

from .base import PlotElementProxy, PlotElement, mark_backend_unsupported
from ..backends import PlotResolver


class ProxyAxis(PlotElementProxy):
    """Proxy for a single axis.

    Handle:
    - scaling
    - bounds

    """

    @mark_backend_unsupported
    def set_axis_scale(self, scale):  # lin, log
        raise NotImplementedError()

    @mark_backend_unsupported
    def set_autoscaling(self, setting: bool):
        pass

    @mark_backend_unsupported
    def set_limits(self, limits):  # Limited to axis with no breaks
        pass

    @mark_backend_unsupported
    def set_limits_with_breaks(self, limits):
        pass

    @mark_backend_unsupported
    def set_label(self, title: str, font: Mapping[str, Any]):
        pass

    @mark_backend_unsupported
    def set_tick_labels(self, labels: Sequence[str], font: Mapping[str, Any]):
        pass


class ProxyColorbar(PlotElementProxy):
    """Proxy for the colorbar attached to a colorplot."""

    pass  # So far expect most manipulatio to happen inside the axis of the colorbar


class ProxyCursor(PlotElementProxy):
    """Proxy for a cursor."""

    pass


class ProxyAxes(PlotElementProxy):
    """Proxy for axes.

    As in matplotlib an axis is expected to provide way to draw into the axis
    and way to manipulate the axis appearance.

    """

    #: Reference to the plot resolver providing implementation for plots.
    #: This architecture allows to extend the kinds of plots supported by a
    #: backend without having to alter its proxy.
    resolver = Typed(PlotResolver)

    @mark_backend_unsupported
    def enable_zooming(self, bound: str, button: str):
        pass

    @mark_backend_unsupported
    def disable_zooming(self):
        pass

    @mark_backend_unsupported
    def enable_panning(self, button: str):
        pass

    @mark_backend_unsupported
    def disable_panning(self):
        pass

    @mark_backend_unsupported
    def add_axis(self, axes=None):
        pass

    @mark_backend_unsupported
    def remove_axis(self):
        pass

    @mark_backend_unsupported
    def add_cursor(
        self, axes=None
    ):  # Need to specify to which axes the cursor is bound
        pass

    @mark_backend_unsupported
    def remove_cursor(self):
        pass

    @mark_backend_unsupported
    def enable_major_grid(self):
        pass

    @mark_backend_unsupported
    def disable_major_grid(self):
        pass

    @mark_backend_unsupported
    def enable_minor_grid(self):
        pass

    @mark_backend_unsupported
    def disable_minor_grid(self):
        pass

    @mark_backend_unsupported
    def set_legend(self, legend: Mapping[str, str]):
        pass

    def add_plot(self, id, plot, axes: Optional[Mapping[str, str]]) -> None:
        """Pass the plot definition to the resolver to be inserted in the axis.

        It is the resolver responsibility to populate the proxy field of the
        definition.

        """
        if axes is None:
            x_axis = self.element.axes["bottom"]
            y_axis = self.element.axes["left"]
        self.resolver.add_plot(self, plot, x_axis=x_axis, y_axis=y_axis)
        if plot.proxy is None:
            raise RuntimeError(
                f"Resolver {self.resolver} failed to populate the proxy of"
                f" the plot {plot} on axis {self.element}."
            )

    @mark_backend_unsupported
    def remove_plot(self, id):
        pass

    @mark_backend_unsupported
    def add_line(
        self,
        id: str,
        orientation: str,
        position: float,
        bounds: Optional[Tuple[float, float]] = None,
    ):
        pass

    @mark_backend_unsupported
    def remove_line(self, id: str) -> None:
        pass


class Axis(PlotElement):
    """Axis of a plot."""

    #: Should that axis be autoscaled
    auto_scaling = Bool()

    #: List of 2 tuple representing a possibly discountinuous axis.
    limits = List(tuple)

    #: Label of the axis
    label = Str()

    #: Tick labels.
    tick_labels = List(str)

    #: Font used for the label
    label_font = Dict(str)

    #: Font used for the tick labels
    tick_labels_font = Dict(str)

    # XXX Add connections to the proxy and a way to prevent self recursion

    # XXX Add convenience to connect axes between them


class AxesSet(NamedTuple):

    bottom: Optional[Axis]
    left: Optional[Axis]
    right: Optional[Axis]
    top: Optional[Axis]


class Cursor(PlotElement):
    """Cursor on a plot."""

    #:
    x_value = Float()

    #:
    y_value = Float()

    #:
    c_value = Float(float("nan"))

    # XXX need to sync to the proxy


class Axes(PlotElement):
    """Axes of a plot"""

    #: Set of axes composing this element
    axes = Typed(AxesSet)

    #: Set of cursors currently active on the graph
    cursors = ATuple(Cursor)

    #: Display a major grid
    major_grid_enabled = Bool()

    #: Display a minor grid
    minor_grid_enabled = Bool()

    #:
    # SHOULD NOT be edited in place.
    legends = Dict(str, str)

    def add_axis(self, position: str):
        pass

    def remove_axis(self, position: str):
        pass

    def add_cursor(self, axes: Tuple[str, str]):  # What axis are we linked to
        pass

    def remove_cursor(self, index: int):
        pass

    # XXX Need to define the proper API to enable zooming/panning and modifiers

    # TODO Add the ability to link axes (accross different figures ie beyond
    # matplotlib default)

    _proxy = Typed(ProxyAxes)
