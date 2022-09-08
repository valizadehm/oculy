# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# ----------------------------------------------------------------------------
"""Model driving the 2D plot panel.

"""
from atom.api import Bool, ForwardTyped, List, Str, Typed, Value
from glaze.utils.atom_util import HasPrefAtom

from oculy.data.datastore import DataStore
from oculy.plotting.plots import Figure, Plot2DRectangularMesh, Plot2DData

from .mask_parameters import MaskParameter


def _workspace():
    from .workspace import SimpleViewerWorkspace

    return SimpleViewerWorkspace


# FIXME add proper metadata to datastore (need to formalize the format)
class Plot2DPanelModel(HasPrefAtom):
    """Model for a 1D plot handling data querying, processing and display."""

    #: Selected entry of the data to use as x axis.
    selected_x_axis = Str()

    #: Selected entry of the data to use as y axis.
    selected_y_axis = Str()

    #: Selected entry of the data to use as c axis.
    selected_c_axis = Str()

    #: Filtering specifications per graph.
    filters = List(MaskParameter)

    #:
    # Allow one pipeline per graph (use a notebook on the UI side)
    pipeline = Value()  # FIXME need a dedicated container

    #: Is auto refresh currently enabled. This attribute reflects the user
    # selection but not necessarily the presence of event handler that can
    # be disabled temporarily when updating.
    auto_refresh = Bool()

    def __init__(self, workspace, datastore):
        self._workspace = workspace
        self._datastore = datastore
        plot_plugin = workspace.workbench.get_plugin("oculy.plotting")
        self._figure = plot_plugin.create_figure(f"SW-2D")
        self._figure.axes_set["default"].add_colorbar()

    def refresh_plot(self) -> None:
        """Force the refreshing of the plot."""
        # Do not plot if there is no selection on some axes
        # NOTE may not be the cleanest way to do this.
        if (
            not self.selected_x_axis
            or not self.selected_y_axis
            or not self.selected_c_axis
        ):
            return
        data = self._workspace._loader.load_data(
            [self.selected_x_axis, self.selected_y_axis, self.selected_c_axis],
            {m.content_id: (m.mask_id, (m.value,)) for m in self.filters},
        )

        # FIXME handle pipeline
        axes = self._figure.axes_set["default"]

        # Update the X axis data
        update = {"sviewer/plot_2d/x":
                      (data[self.selected_x_axis].values, None)}

        # Update the Y axes data
        update["sviewer/plot_2d/y"] = (data[self.selected_y_axis].values, None)

        # Update the C axes data
        update["sviewer/plot_2d/c"] = (data[self.selected_c_axis].values, None)

        # Push a single update
        self._datastore.store_data(update)

        # Create live plots for the newly selected y axes
        if len(axes.plots) == 0:
            pp = self._workspace.workbench.get_plugin("oculy.plotting")
            pp.add_plot(
                f"SW-2D",
                Plot2DRectangularMesh(
                    id=f"SW-2D-{len(axes.plots)}",
                    data=Plot2DData(
                        x=update["sviewer/plot_2d/x"][0],
                        y=update["sviewer/plot_2d/y"][0],
                        c=update["sviewer/plot_2d/c"][0],
                    ),
                ),
                sync_data={
                    "data.x": "sviewer/plot_2d/x",
                    "data.y": "sviewer/plot_2d/y",
                    "data.c": "sviewer/plot_2d/c",
                },
            )

    # --- Private API

    #: Reference to the workspace holding the loader
    _workspace = ForwardTyped(_workspace)

    #: Reference to the application global datastore
    _datastore = Typed(DataStore)

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
            self.observe("selected_x_axis",
                         self._handle_selected_x_axis_change)
            self.observe("selected_y_axis",
                         self._handle_selected_y_axis_change)
            self.observe("selected_c_axis",
                         self._handle_selected_c_axis_change)
            self.observe("filters", self._handle_filters_change)
            for f in self.filters:
                # FIXME redo when exposing all filters
                for n in f.members():
                    f.observe(n, self._handle_filters_change)
            # FIXME handle pipeline
            self.refresh_plot()
        else:
            # Disconnect observers
            self.unobserve("selected_x_axis",
                           self._handle_selected_x_axis_change)
            self.unobserve("selected_y_axis",
                           self._handle_selected_y_axis_change)
            self.unobserve("selected_c_axis",
                           self._handle_selected_c_axis_change)
            self.unobserve("filters", self._handle_filters_change)
            for f in self.filters:
                # FIXME redo when exposing all filters
                for n in f.members():
                    f.unobserve(n, self._handle_filters_change)
            # FIXME handle pipeline

    def _handle_selected_x_axis_change(self, change):
        """Refresh the plot to use the new x axis."""
        self.refresh_plot()

    def _handle_selected_y_axis_change(self, change):
        """Replot data when the selected y axes change."""
        self.refresh_plot()

    def _handle_selected_c_axis_change(self, change):
        """Replot data when the selected y axes change."""
        self.refresh_plot()

    def _handle_filters_change(self, change):
        """Replot data when a filter parameter change."""
        self.refresh_plot()

    def _handle_file_change(self, change):
        """Event handler ensuring that we are in a consistent after a
        file change.

        Used to observe the workspace itself, signaling the begining
        of the change with a True and the end with a False.

        """
        # In the absence of auto refreshing there is nothing to do.
        if not self.auto_refresh:
            return

        self._post_setattr_auto_refresh(change.get("oldvalue"),
                                        change["value"])

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
