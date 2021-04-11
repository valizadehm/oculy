# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Matplotlib proxy for a figure

"""
from atom.api import Bool, Typed
from enaml.application import ScheduledTask, schedule
from enaml.qt.QtCore import Qt
from enaml.qt.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvas

# FIXME used temporarily till we implement a nice tool bar
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure, GridSpec

try:
    from mplcairo.qt import FigureCanvasQTCairo
except ImportError:
    FigureCanvasQTCairo = None

from oculy.plotting.plots import FigureProxy


# FIXME will disappear when we get proper toolbar support
class _TempWidgetPlot(QWidget):
    def __init__(self, parent, proxy):
        QWidget.__init__(self, parent)
        self.setLayout(QVBoxLayout())
        # if FigureCanvasQTCairo is not None and proxy.use_cairo:
        #     canvas = FigureCanvasQTCairo(proxy._figure)
        # else:
        canvas = FigureCanvas(proxy._figure)
        canvas.setParent(self)
        canvas.setFocusPolicy(Qt.ClickFocus)
        canvas.setVisible(True)
        self.toolbar = NavigationToolbar(canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(canvas)
        self.canvas = canvas


class MatplotlibFigureProxy(FigureProxy):
    """Proxy figure for the matplotlib backend"""

    #: Should we use the cairo backend rather than agg
    use_cairo = Bool(True)

    def activate(self):
        """Activate the proxy figure."""
        super().activate()
        self._figure = Figure(figsize=(1, 1), constrained_layout=True)

        grid = self.element.grid
        if len(grid) > 1:
            raise RuntimeError("Multiple axes per figure are not supported yet")
        self.request_redraw()

    def deactivate(self):
        """Deactivate the proxy figure."""
        self._figure.clear()
        for ax in self.element.axes_set.values():
            ax.proxy.deactivate()
        self.request_redraw(clear=True)
        super().deactivate()

    def get_native_widget(self, parent):
        """Get a Qt Canvas to include into the enaml widgets."""
        if self._canvas:
            self._canvas.setParent(parent)
            return self._canvas

        self._canvas = _TempWidgetPlot(parent, self)
        self.request_redraw()

        return self._canvas

    def request_redraw(self, clear: bool = False) -> None:
        """Request to redraw the canvas.

        If the canvas does not exist it is a no-op.

        """
        if not self._canvas or (
            self._redraw_task is not None and (not clear or self._redraw_and_clear)
        ):
            return

        task = self._redraw_task = schedule(self._redraw_handler, (clear,))
        self._redraw_and_clear = clear
        task.notify(self._cleanup_redraw_task)

    # --- Private API

    #: Matplotlib figure driving the display
    _figure = Typed(Figure)

    #: Gridspec used to organize the axes. None if a single axes exist.
    _gridspec = Typed(GridSpec)

    #: Cache for the Canvas holding the figure
    _canvas = Typed(QWidget)

    #: Last request to redraw the canvas.
    _redraw_task = Typed(ScheduledTask)

    #: Was a clear requested as part of the last redraw request
    _redraw_and_clear = Bool()

    def _redraw_handler(self, clear: bool) -> None:
        c = self._canvas.canvas
        if clear:
            self._figure.clear()
        c.draw_idle()
        c.flush_events()

    def _cleanup_redraw_task(self, result: None) -> None:
        self._redraw_and_clear = False
        del self._redraw_task
