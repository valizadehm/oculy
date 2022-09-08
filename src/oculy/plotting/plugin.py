# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Plotting plugin logic.

"""
from collections import defaultdict
from operator import attrgetter
from typing import Mapping, Optional, Tuple

from atom.api import Dict, Str, Typed
from gild.utils.plugin_tools import (
    ExtensionsCollector,
    HasPreferencesPlugin,
    make_extension_validator,
)

from .backends import Backend, BackendResolver
from .plots import Axes, BasePlot, Figure, GridPosition, Plot
from .sync_manager import SyncManager


class PlottingPlugin(HasPreferencesPlugin):
    """Plugin handling plotting of data."""

    #: Default backend to use.
    default_backend = Str("matplotlib").tag(pref=True)

    #: Mapping of figures managed by the plugin. Should not be edited in place.
    figures = Dict(str, Figure)

    #: Manager responsible to handle refreshing the plots linked to the data plugin.
    sync_managers = Dict(BasePlot, SyncManager)

    def start(self):
        """Collect all extensions and generate resolver for each backend."""
        self._plots = ExtensionsCollector(
            workbench=self.workbench,
            point="oculy.plotting.plots",
            ext_class=Plot,
            validate_ext=make_extension_validator(base_cls=Plot, fn_names=("get_cls",)),
        )
        self._plots.start()

        self._backends = ExtensionsCollector(
            workbench=self.workbench,
            point="oculy.plotting.rendering-backends",
            ext_class=Backend,
            validate_ext=make_extension_validator(
                base_cls=Backend,
                attributes=("priority",),
                fn_names=("proxies", "plot_proxies", "colormaps"),
            ),
        )

        self._backends.start()

        self._populate_resolvers()
        self._backends.observe("contributions", self._populate_resolvers)

    def stop(self):
        """Stop plugin."""
        self._backends.unobserve("contributions")
        self._resolvers.clear()
        self._backends.stop()
        self._plots.stop()

    def create_figure(
        self,
        id: str,
        backend: Optional[str] = None,
        axes_positions: Optional[Mapping[str, GridPosition]] = None,
        axes_specifications: Optional[Mapping[str, Optional[Axes]]] = None,
    ) -> Figure:
        """Create a figure with a set of axis.

        Parameters
        ----------
        id : str
            Id of the figure which will be used to refer to it.
        backend: Optional[str], optional
            Id of teh backend to use. Use the plugin global value by default.
        axes_positions : Optional[Mapping[str, GridPosition]]
            Id of each axis and its specific position, default to None which
            will create a single axes for the figure with `default` as id.
        axes_specifications : Optional[Mapping[str, Axes]], optional
            Specification of each axes, default to None which will create
            a left and bottom axis.

        Returns
        -------
        Figure :
            The newly created figure.

        """
        if id in self.figures:
            raise KeyError(f"Figure id {id} already exists.")

        # FIXME validate backend exists
        backend = backend or self.default_backend

        if axes_positions is None:
            axes_positions = {"default": GridPosition(0, 0)}

        if axes_specifications is None:
            axes_specifications = {}

        # FIXME Validate specifications and  positions

        figure = Figure(backend_name=backend)
        for axes_id in axes_positions:
            figure.add_axes(
                axes_id, axes_positions[axes_id], axes_specifications.get(axes_id)
            )
        self.figures[id] = figure

        return figure

    def destroy_figure(self, id: str):
        """Destroy a figure."""
        if id not in self.figures:
            raise KeyError(f"Figure id {id} is not known.")
        fig = self.figures[id]
        del self.figures[id]
        fig.finalize()

    def add_plot(
        self,
        fig_id: str,
        plot: BasePlot,
        axes_id: Optional[str] = None,
        sync_data: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Add a plot a to the specified figure.

        Parameters
        ----------
        fig_id : str
            Id of the figure in which to add the plot.
        plot : BasePlot
            Plot to be added to the figure.
        axes_id : Optional[str], optional
            Id of the axes to which to add the plot. None by default which
            means the plot will be added to the default axes (id: "default").
        axes : Optional[Tuple[str, str]], optional
            Pair of axes to use (ex: "bottom", "left" which the default).
        sync_data : Optional[Mapping[str, str]], optional
            Mapping between attributes of the plot and entries of the data handling
            plugin.

        """
        if fig_id not in self.figures:
            raise KeyError(f"Figure id {fig_id} does not exist.")

        figure = self.figures[fig_id]
        axes_id = "default" if axes_id is None else axes_id
        if axes_id not in figure.axes_set:
            raise KeyError(
                f"Axes id {axes_id} does not exist in figure {fig_id}, "
                f"known axes are {list(figure.axes_set)}"
            )

        ax = figure.axes_set[axes_id]
        if plot.id in ax.plots:
            raise KeyError(
                f"Plot id {plot.id} already exist for axes {axes_id} of figure {fig_id}"
            )

        if sync_data:
            datastore = self.workbench.get_plugin("oculy.data").datastore
            self.sync_managers[plot] = SyncManager(datastore, plot, sync_data)

        ax.add_plot(plot)

    def get_resolver(self, backend_name: str) -> BackendResolver:
        """Access the resolver associated with a given backend."""
        return self._resolvers[backend_name]

    # --- Private API

    #: Contributed backends
    _backends = Typed(ExtensionsCollector)

    #: Contributed plots
    _plots = Typed(ExtensionsCollector)

    #: Resolver for each backend agglomerating all contributions to the backend
    _resolvers = Dict(str, BackendResolver)

    def _populate_resolvers(self):
        """Aggregate contributions made to a single backend name respecting priotities."""
        backends = defaultdict(list)
        for v in self._backends.contributions.values():
            backends[v.id].append(v)

        resolvers = {}
        for name in backends:
            resolver = BackendResolver()
            for contrib in sorted(backends[name], key=attrgetter("priority")):
                resolver.proxies.update(contrib.proxies())
                resolver.proxies.update(contrib.plot_proxies())
                c_colormaps = contrib.colormaps()
                for cat, known in resolver.colormaps.items():
                    known.update(c_colormaps.get(cat, set()))
            resolvers[name] = resolver

        self._resolvers = resolvers
