# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Class to declare a backend.

"""
from typing import Dict, List, Type

from atom.api import Int, Str
from enaml.core.api import Declarative, d_, d_func

from ..plots.base import BasePlot, BasePlotProxy, PlotElement, PlotElementProxy


class Backend(Declarative):
    """Declaration of a backend contributed to "oculy.plotting.rendering-backend"."""

    #: Name of the backend
    id = d_(Str())

    #: Short description of the backend.
    description = d_(Str())

    #: Priority of the backend contributions.
    #: Used if multiple declaration refer to the same backend, higher number have
    #: higher priority.
    priority = Int(50)

    @d_func
    def proxies(self) -> Dict[Type[PlotElement], Type[PlotElementProxy]]:
        """Overwrite to provide proxies implementation for generic elements."""
        raise NotImplementedError

    @d_func
    def plot_proxies(self) -> Dict[Type[BasePlot], Type[BasePlotProxy]]:
        """Overwrite to provide proxies implementation for plots."""
        raise NotImplementedError

    @d_func
    def colormaps(self) -> Dict[str, List[str]]:
        """Overwrite to provide the colormaps supported by the backend.

        The expected keys of the dictionary are:

        - "Perceptually uniform"
        - "Sequential"
        - "Diverging"

        """
        raise NotImplementedError
