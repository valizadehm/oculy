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
from enaml.qt.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar,,  # FIXME used temporarily till we implement a nice tool bar
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
        if FigureCanvasQTCairo is not None and proxy.use_cairo:
            self.canvas = FigureCanvasQTCairo(proxy._figure)
        else:
            self.canvas = FigureCanvas(proxy._figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)


class MatplotlibFigureProxy(FigureProxy):
    """Proxy figure for the matplotlib backend"""

    #: Should we use the cairo backend rather than agg
    use_cairo = Bool(True)

    def activate(self):
        """Activate the proxy figure."""
        self._figure = Figure(constrained_layout=True)

        grid = self.element.grid
        if len(grid) > 1:
            raise RuntimeError("Multi-axes per figure are not supported yet")

    def deactivate(self):
        """Deactivate the proxy figure."""
        self._figure.clear()

    def get_native_widget(self, parent):
        """Get a Qt Canvas to include into the enaml widgets."""
        if self._canvas:
            self._canvas.setParent(parent)
            return self._canvas

        self._canvas = _TempWidgetPlot(parent, self)

        return self._canvas

    # --- Private API

    #: Matplotlib figure driving the display
    _figure = Typed(Figure)

    #: Gridspec used to organize the axes. None if a single axes exist.
    _gridspec = Typed(GridSpec)

    #: Cache for the Canvas holding the figure
    _canvas = Typed(QWidget)
