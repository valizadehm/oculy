# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# ----------------------------------------------------------------------------
"""Model driving the 1D plot panel.

"""
from atom.api import Bool, ForwardTyped, Int, List, Str, Typed, Value
from gild.utils.atom_util import HasPrefAtom

from oculy.data.datastore import DataStore
from oculy.plotting.plots import Figure, Plot1DLine, Plot1DData

from .mask_parameters import MaskParameter


def _workspace():
    from .workspace import SimpleViewerWorkspace

    return SimpleViewerWorkspace


# FIXME add proper metadata to datastore (need to formalize the format)
class Plot1DModel(HasPrefAtom):
    """Model for a 1D plot handling data querying, processing and display."""

    #: Selected entry of the data to use as x axis for each plot.
    selected_x_axis = Str()

    #: Entries to use on y axis of each plot.
    selected_y_axes = List(str)

    #: Filtering specifications per graph.
    filters = List(MaskParameter)

    #:
    # Allow one pipeline per graph (use a notebook on the UI side)
    pipeline = Value()  # FIXME need a dedicated container

    #: Is auto refresh currently enabled. This attribute reflects the user
    # selection but not necessarily the presence of event handler that can
    # be disabled temporarily when updating.
    auto_refresh = Bool()

    def __init__(self, index, workspace, datastore):
        self._workspace = workspace
        self._index = index
        self._datastore = datastore
        plot_plugin = workspace.workbench.get_plugin("oculy.plotting")
        self._figure = plot_plugin.create_figure(f"SW-1D-{index}")

    def refresh_plot(self) -> None:
        """Force the refreshing of the plot."""
        # Do not plot if there is no selection on some axes
        # NOTE may not be the cleanest way to do this.
        if not self.selected_x_axis or not self.selected_y_axes:
            return
        data = self._workspace._loader.load_data(
            [self.selected_x_axis] + self.selected_y_axes,
            {m.content_id: (m.mask_id, (m.value,)) for m in self.filters},
        )

        # FIXME handle pipeline
        axes = self._figure.axes_set["default"]
        # Update the X axis data
        update = {
            f"sviewer/plot_1d_{self._index}/x": (
                data[self.selected_x_axis].values,
                None,
            )
        }
        # Update the Y axes data
        update.update(
            {
                # FIXME set metadata to indicate data origin
                f"sviewer/plot_1d_{self._index}/y_{i}": (
                    data[y_name].values,
                    None,
                )
                for i, y_name in enumerate(self.selected_y_axes)
            }
        )
        # Delete data for axes that do not exist anymore
        if len(axes.plots) > len(self.selected_y_axes):
            update.update(
                {
                    # FIXME set metadata to indicate data origin
                    f"sviewer/plot_1d_{self._index}/y_{i}": (None, None)
                    for i in range(len(self.selected_y_axes), len(axes.plots))
                }
            )

        # Push a single update
        self._datastore.store_data(update)

        # Create live plots for the newly selected y axes
        if len(axes.plots) < len(self.selected_y_axes):
            pp = self._workspace.workbench.get_plugin("oculy.plotting")
            for i in range(len(axes.plots), len(self.selected_y_axes)):
                pp.add_plot(
                    f"SW-1D-{self._index}",
                    Plot1DLine(
                        id=f"SW-1D-{self._index}-{len(axes.plots)}",
                        data=Plot1DData(
                            x=update[f"sviewer/plot_1d_{self._index}/x"][0],
                            y=update[
                                f"sviewer/plot_1d_{self._index}/" f"y_{i}"
                            ][0],
                        ),
                    ),
                    sync_data={
                        "data.x": f"sviewer/plot_1d_{self._index}/x",
                        "data.y": f"sviewer/plot_1d_{self._index}/y_{i}",
                    },
                )

    # --- Private API

    #: Reference to the workspace holding the loader
    _workspace = ForwardTyped(_workspace)

    #: Reference to the application global datastore
    _datastore = Typed(DataStore)

    #: Index of the panel identifying its data in the datastore and its figure
    #: in the plotting plugin.
    _index = Int()

    #: Reference to the figure being displayed
    _figure = Typed(Figure)

    #: Is auto refresh currently enabled at this instant.
    _auto_refresh = Bool()

    # --- Event handling

    def _post_setattr_auto_refresh(self, old, new) -> None:
        """Connect observers to auto refresh when a plot input parameter
        change."""
        self._auto_refresh = new

        if new:
            # Connect observers
            self.observe(
                "selected_x_axis", self._handle_selected_x_axis_change
            )
            self.observe(
                "selected_y_axes", self._handle_selected_y_axes_change
            )
            self.observe("filters", self._handle_filters_change)
            for f in self.filters:
                # FIXME redo when exposing all filters
                for n in f.members():
                    f.observe(n, self._handle_filters_change)
            # FIXME handle pipeline
            self.refresh_plot()
        else:
            # Disconnect observers
            self.unobserve(
                "selected_x_axis", self._handle_selected_x_axis_change
            )
            self.unobserve(
                "selected_y_axes", self._handle_selected_y_axes_change
            )
            self.unobserve("filters", self._handle_filters_change)
            for f in self.filters:
                # FIXME redo when exposing all filters
                for n in f.members():
                    f.unobserve(n, self._handle_filters_change)
            # FIXME handle pipeline

    def _handle_selected_x_axis_change(self, change):
        """Refresh the plot to use the new x axis."""
        if not change["value"]:
            return
        # Get and filter the data as requested
        data = self._workspace._loader.load_data(
            [change["value"]],
            {m.mask_id: (m.content_id, m.value) for m in self.filters},
        )
        # Extract the inner numpy array
        new_x = data[change["value"]].values

        # FIXME handle pipeline

        self._datastore.store_data(
            {f"sviewer/plot_1d_{self._index}/x": (new_x, None)}
        )

    def _handle_selected_y_axes_change(self, change):
        """Replot data when the selected y axes change."""
        self.refresh_plot()

    def _handle_filters_change(self, change):
        """Replot data when a filter parameter change."""
        self.refresh_plot()

    def _handle_file_change(self, change):
        """Event handler ensuring that we are in a consistent after a file
        change.

        Used to observe the workspace itself, signaling the begining of
        the change with a True and the end with a False.

        """
        # In the absence of auto refreshing there is nothing to do.
        if not self.auto_refresh:
            return

        self._post_setattr_auto_refresh(
            change.get("oldvalue"), change["value"]
        )

    # Filter manipulations

    def _add_filter(self, index: int, position: str) -> None:
        """ """
        filters = self.filters[:]
        if position == "before":
            filters.insert(index, MaskParameter())
        elif position == "after":
            if index + 1 == len(filters):
                filters.append(MaskParameter())
            else:
                filters.insert(index + 1, MaskParameter())
        else:
            raise ValueError(
                f"Got invalid position: {position}, "
                f"expected 'before' or 'after'"
            )
        self.filters = filters

    def _remove_filter(self, index: int) -> None:
        """ """
        filters = self.filters[:]
        del filters[index]
        self.filters = filters


class Plot1DPanelModel(HasPrefAtom):
    """Model representing the current state of the 1D plots panel."""

    #: Model representing the state of each figure.
    models = List()

    #: Should any change to a parameter lead to an automatic replot.
    auto_refresh = Bool()

    #:
    # NOTE use more memory by caching intermediate results
    optimize_for_speed = Bool()

    def __init__(self, workspace, datastore):
        self.models = [Plot1DModel(i, workspace, datastore) for i in range(1)]

    def _post_setattr_auto_refresh(self, old, new):
        """"""
        if new:
            for m in self.models:
                m.auto_refresh = True
                m.refresh_plot()
        else:
            for m in self.models:
                m.auto_refresh = False

    def _post_setattr_optimize_for_speed(self, old, new):
        """"""
        # FIXME clean any existing cache when disabling
        #  (currently there is no cache)
        pass
