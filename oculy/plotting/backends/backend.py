# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Class to declare a backend.

"""
from atom.api import Str
from enaml.core.api import Declarative, d_, d_func


class Backend(Declarative):
    """Declaration of a backend contributed to "oculy.plotting.rendering-backend"."""

    #: Name of the backend
    name = d_(Str())

    @d_func
    def proxies(self):
        """Overwrite to provide proxies implementation for generic elements."""
        raise NotImplementedError

    @d_func
    def plot_proxies(self):
        """Overwrite to provide proxies implementation for plots."""
        raise NotImplementedError

    @d_func
    def colormaps(self):
        """Overwrite to provide the list of colormap supported by the backend."""
        raise NotImplementedError
