# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Axis, axes, colorbar and their associated proxy.

"""
from typing import Any, Optional, Sequence, Tuple, Mapping

from atom.api import (
    Str,
    ForwardTyped,
    Typed,
    Bool,
    List,
    Dict,
    Float,
    Tuple as ATuple,
    Enum,
    Int,
)

from .base import BasePlot, PlotElementProxy, PlotElement, mark_backend_unsupported
from ..backends.resolver import BackendResolver


class AxisProxy(PlotElementProxy):
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
    def invert_axis(self, state: bool):
        pass

    @mark_backend_unsupported
    def set_label(self, title: str, font: Mapping[str, Any]):
        pass

    @mark_backend_unsupported
    def set_tick_labels(self, labels: Sequence[str], font: Mapping[str, Any]):
        pass

    @mark_backend_unsupported
    def set_tick_position(self, position: str):
        pass


class ColorbarProxy(PlotElementProxy):
    """Proxy for the colorbar attached to a colorplot."""

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


class CursorProxy(PlotElementProxy):
    """Proxy for a cursor."""

    pass


class AxesProxy(PlotElementProxy):
    """Proxy for axes.

    As in matplotlib an axis is expected to provide way to draw into the axis
    and way to manipulate the axis appearance.

    """

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
    def set_projections(self):
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

    #: Reference to the parent axes.
    axes = ForwardTyped(lambda: Axes)

    #: Should that axis be autoscaled
    auto_scaling = Bool()

    #: List of 2 tuple representing a possibly discountinuous axis.
    limits = List(tuple)

    #: Is the axis direction inverted.
    inverted = Bool()

    #: Label of the axis
    label = Str()

    #: Tick labels.
    tick_labels = List(str)

    #: Font used for the label
    label_font = Dict(str)

    #: Font used for the tick labels
    tick_labels_font = Dict(str)

    #: Intercept position of this axis with the other axis in data coordinate.
    #: Setting this values will have an impact only if there are only 2 active
    #: axes in the axes_set.
    intercept = Float()

    # XXX Add connections to the proxy and a way to prevent self recursion

    # XXX Add convenience to connect axes between them


class Colorbar(PlotElement):
    """Colorbar for a 2D plot."""

    #: Reference to the parent axes.
    axes = ForwardTyped(lambda: Axes)

    #: Position at which the colorbar should be created.
    location = Enum(("right", "top", "left", "bottom"))

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

    #:
    aspect_ratio = Int(20)


class Cursor(PlotElement):
    """Cursor on a plot."""

    #:
    x_value = Float()

    #:
    y_value = Float()

    #:
    c_value = Float(float("nan"))

    # XXX need to sync to the proxy


def _resolve_figure():
    from .figure import Figure

    return Figure


class Axes(PlotElement):
    """Axes of a plot"""

    #: Reference to the figure holding the axes.
    figure = ForwardTyped(_resolve_figure)

    #: Axes composing this object.
    left_axis = Typed(Axis)
    bottom_axis = Typed(Axis)
    right_axis = Typed(Axis)
    top_axis = Typed(Axis)

    #: Colorbar associated with plot if any.
    colorbar = Typed(Colorbar)

    #: Set of cursors currently active on the graph
    cursors = ATuple(Cursor)

    #: Set of plots currently displayed in the axes
    plots = ATuple(BasePlot)

    #: Display a major grid
    major_grid_enabled = Bool()

    #: Display a minor grid
    minor_grid_enabled = Bool()

    #:
    # SHOULD NOT be edited in place.
    legends = Dict(str, str)

    #: Projection to use on the axes.
    projection = Enum(("cartesian", "polar"))

    def initialize(self, resolver):
        """Initialize the proxy of the object and the axes."""
        self._resolver = resolver
        super().initialize(resolver)
        for axis in (self.left_axis, self.bottom_axis, self.right_axis, self.top_axis):
            axis.backend_name = self.backend_name
            axis.initialize(resolver)
        if self.colorbar:
            self.colorbar.backend_name = self.backend_name
            self.colorbar.initialize(resolver)
        for c in self.cursors:
            c.backend_name = self.backend_name
            c.initialize(resolver)
        for p in self.plots:
            p.backend_name = self.backend_name
            p.initialize(resolver)

        #: Conserve
        self._plugin

    def finalize(self):
        """Finalize the proxy of the figure."""
        for p in self.plots:
            p.finalize()
        for c in self.cursors:
            c.finalize()
        if self.colorbar:
            self.colorbar.finalize()
        for axis in (self.top_axis, self.right_axis, self.bottom_axis, self.left_axis):
            axis.finalize()
        super().finalize()

    def add_cursor(self, axes: Tuple[str, str]):  # What axis are we linked to
        pass

    def remove_cursor(self, index: int):
        pass

    def add_plot(self, plot) -> None:
        """Add a plot to the axes."""
        if plot.id in self.plots:
            raise RuntimeError(f"A plot with {id} already exist in axes {self}")

        axes = plot.axes_mapping
        if axes is None:
            axes = {
                "x": "bottom" if self.element.bottom_axis else "top",
                "y": "left" if self.element.left_axis else "right",
            }

        # Validate the axes supposed to be used.
        if any(
            (
                pa not in ("left", "bottom", "right", "top")
                or getattr(axes, f"{pa}_axis") is None
            )
            for pa in axes.values()
        ):
            unknown = []
            missing = []
            for lab, pa in axes.items():
                if pa not in ("left", "bottom", "right", "top"):
                    unknown.append((lab, pa))
                elif getattr(axes, f"{pa}_axis") is None:
                    missing.append((lab, pa))
            if missing:
                raise RuntimeError(
                    f"The axes used for {[lab for lab, _ in unknown]} do not "
                    "correspond to any valid axes (valid axes are "
                    "'left', 'right', 'top', 'bottom', provided axes are "
                    f"{[pa for _, pa in unknown]})."
                )
            else:
                raise RuntimeError(
                    f"The axes used for {[lab for lab, _ in missing]} do not "
                    "exist. Existing axes are "
                    f"{[ax for ax in axes.axes._fields if axes.axes[ax] is not None]}, "
                    f"specified axes are {[pa for _, pa in missing]}."
                )

        # Create a proxy
        self._resolver.resolve_proxy(self, plot, axes)

        # Make sure the plot knows where it is plotted.
        plot.axes = self
        self.plots[plot.id] = plot

        # Activate teh proxy
        plot.proxy.activate

    def remove_plot(self, id):
        """Remove a plot based on its ID."""
        if id not in self.plots:
            raise KeyError(
                f"Plot {id} does not exist in axes {self.axes},"
                f" known plots are {self.plots}"
            )
        if not self.proxy:
            raise RuntimeError(f"Axes {self} does not have an active proxy.")
        self.proxy.remove_plot(id, self.plots[id])

    def add_colorbar(self):
        """"""
        pass

    def remove_colorbar(self):
        """"""
        pass

    def add_line(
        self,
        id: str,
        orientation: str,
        position: float,
        bounds: Optional[Tuple[float, float]] = None,
    ):
        pass

    def remove_line(self, id: str) -> None:
        pass

    # XXX Need to define the proper API to enable zooming/panning and modifiers

    # TODO Add the ability to link axes (accross different figures ie beyond
    # matplotlib default)

    # --- Private API

    #: Reference to the backend resolver needed to dynamically add axes
    _resolver = Typed(BackendResolver)
