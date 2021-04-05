# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Matplotlib proxy for axis, axes, colorbar and cursor.

"""
from atom.api import Dict, Typed
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.colorbar import make_axes

from oculy.plotting.plots import AxesProxy, AxisProxy, ColorbarProxy, CursorProxy


class MatplotlibAxisProxy(AxisProxy):
    """Matplotlib proxy for a single axis."""

    def activate(self):
        """Activate the proxy axis."""
        el = self.element
        axes = self.element.axes

        if axes is None:
            raise RuntimeError("Cannot activate the proxy for an Axis with no axes")

        # Identify direction
        ax_dir = ""
        for direction in ("left", "bottom", "right", "top"):
            if getattr(axes, f"{direction}_axis") is el:
                ax_dir = direction
                break

        if not ax_dir:
            raise RuntimeError("Axis does not exist on parent Axes object")

        if ax_dir in ("bottom", "top"):
            for c in ("left", "right"):
                if (ax_dir, c) in axes.proxy._axes:
                    self._axis = axes.proxy._axes[(ax_dir, c)].xaxis
        else:
            for c in ("bottom", "top"):
                if (c, ax_dir) in axes.proxy._axes:
                    self._axis = axes.proxy._axes[(c, ax_dir)].yaxis

        if not self._axis:
            raise RuntimeError("Failed to find backend axis.")

    def deactivate(self):
        """Deactivate the proxy figure."""
        del self._axis

    # @mark_backend_unsupported
    # def set_axis_scale(self, scale):  # lin, log
    #     raise NotImplementedError()

    # @mark_backend_unsupported
    # def set_autoscaling(self, setting: bool):
    #     pass

    # @mark_backend_unsupported
    # def set_limits(self, limits):  # Limited to axis with no breaks
    #     pass

    # @mark_backend_unsupported
    # def set_limits_with_breaks(self, limits):
    #     pass

    # @mark_backend_unsupported
    # def invert_axis(self, state: bool):
    #     pass

    # @mark_backend_unsupported
    # def set_label(self, title: str, font: Mapping[str, Any]):
    #     pass

    # @mark_backend_unsupported
    # def set_tick_labels(self, labels: Sequence[str], font: Mapping[str, Any]):
    #     pass

    # --- Private API

    _axis = Typed(Axis)


class MatplotlibColorbarProxy(ColorbarProxy):
    """Matplotlib proxy for a colorbar."""

    def activate(self):
        """Activate the proxy colorbar."""
        # Create matplotlib axes which will hold the colorbar.
        axes = tuple(self.element.axes.proxy._axes)[0]
        self._caxes = make_axes(
            axes, location=self.element.location, aspect=self.element.aspect_ratio
        )

    def deactivate(self):
        """Deactivate the proxy colorbar."""
        self._caxes.clear()
        del self._caxes

    def connect_mappable(self, mappable):
        """Create a new colorbar for a mappable."""
        self._caxes.clear()
        self.element.axes.figure.proxy._figure.colorbar(mappable, self._caxes)

    # @mark_backend_unsupported
    # def set_axis_scale(self, scale):  # lin, log
    #     raise NotImplementedError()

    # @mark_backend_unsupported
    # def set_autoscaling(self, setting: bool):
    #     pass

    # @mark_backend_unsupported
    # def set_limits(self, limits):  # Limited to axis with no breaks
    #     pass

    # @mark_backend_unsupported
    # def set_limits_with_breaks(self, limits):
    #     pass

    # @mark_backend_unsupported
    # def set_label(self, title: str, font: Mapping[str, Any]):
    #     pass

    # @mark_backend_unsupported
    # def set_tick_labels(self, labels: Sequence[str], font: Mapping[str, Any]):
    #     pass

    # --- Private API

    _caxis = Typed(Axes)


# FIXME implement later
class MatplotlibCursorProxy(CursorProxy):
    """"""

    pass


class MatplotlibAxesProxy(AxesProxy):
    """Matplotlib proxy for axes."""

    def activate(self):
        """Activate the proxy axes."""
        super().activate()
        el = self.element
        fig = el.figure
        if len(fig.axes_set) > 1:
            raise RuntimeError()  # Add support for more than one axis.
        else:
            first_axes = fig.proxy._figure.add_subplot(
                projection=el.projection if el.projection != "cartesian" else None,
            )
            first_axes.set_autoscale_on(True)

        active_axes = {
            direction: getattr(el, f"{direction}_axis")
            for direction in ("left", "bottom", "right", "top")
            if getattr(el, f"{direction}_axis")
        }

        if len(active_axes) == 2:
            if "right" in active_axes:
                first_axes.yaxis.set_tick_position("right")
            if "top" in active_axes:
                first_axes.xaxis.set_tick_position("top")
            self._axes = {
                (
                    "bottom" if "bottom" in active_axes else "top",
                    "left" if "left" in active_axes else "right",
                ): first_axes
            }
        else:
            raise RuntimeError("Support is currently limited to 2 axes")
        self.element.figure.proxy.request_redraw()

    def deactivate(self):
        """Deactivate the proxy axes."""
        self._axes.clear()
        del self._axes
        super().deactivate()

    def get_default_axes_mapping(self):
        """Get teh default axes mapping for plots."""

    # @mark_backend_unsupported
    # def enable_zooming(self, bound: str, button: str):
    #     pass

    # @mark_backend_unsupported
    # def disable_zooming(self):
    #     pass

    # @mark_backend_unsupported
    # def enable_panning(self, button: str):
    #     pass

    # @mark_backend_unsupported
    # def disable_panning(self):
    #     pass

    # @mark_backend_unsupported
    # def add_axis(self, axes=None):
    #     pass

    # @mark_backend_unsupported
    # def remove_axis(self):
    #     pass

    # @mark_backend_unsupported
    # def set_projections(self):
    #     pass

    # @mark_backend_unsupported
    # def add_cursor(
    #     self, axes=None
    # ):  # Need to specify to which axes the cursor is bound
    #     pass

    # @mark_backend_unsupported
    # def remove_cursor(self):
    #     pass

    # @mark_backend_unsupported
    # def enable_major_grid(self):
    #     pass

    # @mark_backend_unsupported
    # def disable_major_grid(self):
    #     pass

    # @mark_backend_unsupported
    # def enable_minor_grid(self):
    #     pass

    # @mark_backend_unsupported
    # def disable_minor_grid(self):
    #     pass

    # @mark_backend_unsupported
    # def set_legend(self, legend: Mapping[str, str]):
    #     pass

    # @mark_backend_unsupported
    # def remove_plot(self, id):
    #     pass

    # @mark_backend_unsupported
    # def add_line(
    #     self,
    #     id: str,
    #     orientation: str,
    #     position: float,
    #     bounds: Optional[Tuple[float, float]] = None,
    # ):
    #     pass

    # @mark_backend_unsupported
    # def remove_line(self, id: str) -> None:
    #     pass

    #: --- Private API

    _axes = Dict(tuple, Axes)
