# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Base class for plot resolver in charge of handling plotting for each class of plot.

"""
from atom.api import Atom, Dict, Str, Typed
from enaml.workbench.api import Workbench

from ..plots.base import PlotElement, PlotElementProxy


class BackendResolver(Atom):
    """Base plot resolver."""

    #: Instance of the application workbench.
    workbench = Typed(Workbench)

    #: Name of the backend for this resolver instance is used with
    backend_name = Str()

    #: Backend specific proxies.
    proxies = Dict(PlotElement, PlotElementProxy)

    #: Valid colormaps for the backend by category.
    colormaps = Dict(str, str)

    def resolve_proxy(self, element: PlotElement) -> PlotElementProxy:
        """Resolve and create the proxy for an element."""
        el_type = type(element)

        if el_type not in self.proxies:
            raise RuntimeError(
                f"Plot type {el_type} is not supported by {self.backend_name}, "
                f"proxies are implemented for {list(self.proxies)}"
            )

        proxy = self.proxies[el_type](element=element)
        element.proxy = proxy
        return proxy

    # --- Private API

    def _default_colormaps(self):
        """Provide the standard colormap categories."""
        return {"Perceptually uniform": set(), "Sequential": set(), "Diverging": set()}
