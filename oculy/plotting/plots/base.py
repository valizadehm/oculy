# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Base classes for plotting element using a proxy.

"""
from atom.api import Atom, ForwardTyped, Typed, Str, Subclass
from enaml.core.api import Declarative, d_, dfunc


def mark_backend_unsupported(func):
    """Mark a method as being not supported by a backend."""
    func._oculy_backend_unsupported = True
    return func


class PlotElementProxy(Atom):
    """Proxy for a plot element providing a uniform interface accross backends."""

    #: Reference to the element holding this proxy
    element = ForwardTyped(lambda: PlotElement)


class PlotElement(Atom):
    """Element of plot interacting with the backend through a proxy."""

    #: Backend specific proxy
    proxy = Typed(PlotElementProxy)


class BasePlotProxy(PlotElementProxy):
    """"""

    pass


class BasePlot(PlotElement):
    """"""

    pass


# declarative part for a plot
class Plot:

    #:
    id = d_(Str())

    #:
    @dfunc
    def get_cls(self) -> BasePlot:
        pass
