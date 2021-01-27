# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Matplotlib proxy for axis, axes, colorbar and cursor.

"""
from atom.api import Typed
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.cm import ScalarMappable

from oculy.plotting.plots import AxisProxy, AxesProxy, ColorbarProxy, CursorProxy


class MatplotlibAxisProxy(AxisProxy):
    """Matplotlib proxy for a single axis."""

    def activate(self):
        """Activate the proxy axis."""
        pass

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
        # XXX Apply attributes states

    def deactivate(self):
        """Deactivate the proxy colorbar."""
        self._axes.clear()
        del self._axes

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

    _colorbar = Typed()


# XXX implement later
class MatplotlibCursorProxy(CursorProxy):
    """"""

    pass


class MatplotlibAxesProxy(AxesProxy):
    """Matplotlib proxy for axes."""

    def activate(self):
        """Activate the proxy axes."""
        el = self.element
        fig = el.figure
        if len(fig.axes_set) > 1:
            raise RuntimeError()  # Add support for more than one axis.
        else:
            self._axes = fig.proxy._figure.gca()
        # XXX Apply attributes states

    def deactivate(self):
        """Deactivate the proxy axes."""
        self._axes.clear()
        del self._axes

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

    _axes = Typed(Axes)
