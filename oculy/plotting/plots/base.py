# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Base classes for plotting element using a proxy.

"""
from atom.api import Atom, Bool, ForwardTyped, Typed, Str, Value
from enaml.core.api import Declarative, d_, dfunc


def mark_backend_unsupported(func):
    """Mark a method as being not supported by a backend."""
    func._oculy_backend_unsupported = True
    return func


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

    # XXX
    visibility = Bool(True)

    def initialize(self, plugin):
        """Initialize the element by creating the proxy."""
        proxy = plugin.resolve(self, self.backend_name)
        self.proxy = proxy
        proxy.element = self
        proxy.activate()

    def finalize(self):
        """Finalize the element by destroying the proxy."""
        self.proxy.deactivate()
        del self.proxy.element
        del self.proxy


class BasePlotProxy(PlotElementProxy):
    """"""

    def refresh(self):
        """Request a backend redraw."""
        raise NotImplementedError


class BasePlot(PlotElement):
    """Base class for plot description."""

    #: Reference to the data vault holding all the data.
    data_vault = Value()  # XXX add better typing later


# declarative part for a plot
class Plot(Declarative):

    #:
    id = d_(Str())

    #:
    @dfunc
    def get_cls(self) -> BasePlot:
        pass
