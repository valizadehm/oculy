# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Base classes for plotting element using a proxy.

"""
from atom.api import Atom, Bool, ForwardTyped, Typed, Str, Dict, Int
from enaml.core.api import Declarative, d_, dfunc


def mark_backend_unsupported(func):
    """Mark a method as being not supported by a backend."""
    func._oculy_backend_unsupported = True
    return func


def update_proxy(self, change):
    """Update the proxy when the data changes."""
    if self.proxy and self.proxy.is_active:
        handler = getattr(self.proxy, "set_" + change["name"], None)
        if handler is not None:
            handler(change["value"])


class PlotElementProxy(Atom):
    """Proxy for a plot element providing a uniform interface accross backends."""

    #: Reference to the element holding this proxy
    element = ForwardTyped(lambda: PlotElement)

    #: Is the proxy active.
    is_active = Bool()

    def activate(self) -> None:
        """Activate the proxy."""
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate the proxy."""
        self.is_active = False

    @mark_backend_unsupported
    def set_visibility(self, visibility: bool):
        pass


class PlotElement(Atom):
    """Element of plot interacting with the backend through a proxy."""

    #: Name of the backend to use
    backend_name = Str()

    #: Backend specific proxy
    proxy = Typed(PlotElementProxy)

    #: Control the visibility of the element.
    visibility = Bool(True)

    def initialize(self, resolver):
        """Initialize the element by creating the proxy."""
        proxy = resolver.resolve(self, self.backend_name)
        proxy.activate()
        self.observe("visibility", update_proxy)

    def finalize(self):
        """Finalize the element by destroying the proxy."""
        self.unobserve("visibility", update_proxy)
        self.proxy.deactivate()
        del self.proxy.element
        del self.proxy


class BasePlotProxy(PlotElementProxy):
    """Base proxy for plots."""

    pass


def _axes():
    from .axes import Axes

    return Axes


class BasePlot(PlotElement):
    """Base class for plot description."""

    #: Id of the plot used to identify it in an axes
    id = Str()

    #: Reference to the axes to which this plot belongs (or None)
    axes = ForwardTyped(_axes)

    #: What axes ("left", "bottom", etc) to use for "x", "y" ("x" acts as key)
    axes_mapping = Dict(str, str)

    #: Z order determining the order in which the plots are drawn.
    #: Smaller values are drawn first.
    zorder = Int(10)


class InvalidPlotData(Exception):
    """Signal that data provided to drive a plot do not match the expectations."""

    pass


# declarative part for a plot
class Plot(Declarative):

    #:
    id = d_(Str())

    #:
    @dfunc
    def get_cls(self) -> BasePlot:
        pass
