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
from enaml.qt.QtWidgets import QWidget, QVBoxLayout
from matpltolib.figure import Figure, Gridspec
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,  # XXX used temporarily till we implement a nice tool bar
)

try:
    from mplcairo.qt import FigureCanvasQTCairo
except ImportError:
    FigureCanvasQTCairo = None

from oculy.plotting.plots import FigureProxy


# XXX will disappear when we get proper toolbar support
class _TempWidgetPlot(QWidget):
    def __init__(self, parent, proxy):
        QWidget.__init__(self, parent)
        self.setLayout(QVBoxLayout())
        if FigureCanvasQTCairo is not None and self.use_cairo:
            self.canvas = FigureCanvasQTCairo(self._figure, self)
        else:
            self.canvas = FigureCanvas(self._figure, self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)


class MatplotlibFigureProxy(FigureProxy):
    """Proxy figure for the matplotlib backend"""

    #: Should we use the cairo backend rather than agg
    use_cairo = Bool()

    def activate(self):
        """Activate the proxy figure."""
        self._figure = Figure(constrained_layout=True)

        grid_elements = self.element.grid
        if grid_elements:
            raise RuntimeError("Unsupported")

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
    _gridspec = Typed(Gridspec)

    #: Cache for the Canvas holding the figure
    _canvas = Typed(QWidget)
