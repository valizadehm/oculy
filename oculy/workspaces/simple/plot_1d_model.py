# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Model driving the 1D plot panel.

"""
from atom.api import Atom, Bool, List, Str, Typed, ForwardTyped, Int
from glaze.utils.atom_util import HasPreferencesAtom

from oculy.data.datastore import DataStore
from oculy.plotting.plots import Figure
from .mask_parameters import MaskParameter


def _workspace():
    from .workspace import SimpleViewerWorkspace

    return SimpleViewerWorkspace


# FIXME add proper metadata to datastore (need to formalize the format)
# XXX handle addition of new lines to the figure
# XXX implement __init__
class Plot1DModel(Atom):
    """Model for a 1D plot hadnling data querying, processing and display."""

    #: Selected entry of the data to use as x axis for each plot.
    selected_x_axis = Str()

    #: Entries to use on y axis of each plot.
    selected_y_axes = List(str)

    #: Filtering specifications per graph.
    filters = List(MaskParameter)

    #:
    # Allow one pipeline per graph (use a notebook on the UI side)
    pipeline = Typed()  # XXX need a dedicated container

    #: Is auto refresh currently enabled. This attribute reflects the user selection
    #: but not necessarily the presence of event handler that can be disabled
    #: temporarily when updating.
    auto_refresh = Bool()

    def __init__(self, index, workspace, datastore):
        # XXX Create the figure, and store the datastore.
        pass

    def refresh_plot(self) -> None:
        """Force the refreshing of the plot."""
        data = self._workspace._loader.load_data(
            [self.selected_x_axis] + self.selected_y_axes,
            {m.mask_id: (m.content_id, m.value) for m in self.filters},
        )

        # FIXME handle pipeline

        update = {
            f"sviewer/plot_1d_{self._index}/x": (
                data[self.selected_y_axes].values,
                None,
            )
        }
        update.update(
            {
                # XXX set metadata to indicate data origin
                f"sviewer/plot_1d_{self._index}/y_{i}": (data[y_name].values, None)
                for i, y_name in enumerate(self.selected_y_axes)
            }
        )
        self._datastore.store_data(update)

        # XXX handle adding new line plots if relevant

    # --- Private API

    #: Reference to the worspace holding the loader
    _workspace = ForwardTyped(_workspace)

    #: Reference to the application global datastore
    _datastore = Typed(DataStore)

    #: Index of the panel identifying it the datastore.
    _index = Int()

    #: Reference to the figure being displayed
    _figure = Typed(Figure)

    #: Is auto refresh currently enabled at this instant.
    _auto_refresh = Bool()

    # Event handling

    def _post_setattr_auto_refresh(self, old, new) -> None:
        """Connect observers to auto refresh when a plot input parameter change."""
        self._auto_refresh = new

        if new:
            # Connect observers
            self.observe("selected_x_axis", self._handle_selected_x_axis_changed)
            self.observe("selected_y_axes", self._handle_selected_x_axes_changed)
            self.observe("filters", self._handle_filters_change)
            for f in self.filters:
                # FIXME redo when exposing all filters
                for n in f.members():
                    f.observe(n, self._handle_filters_change)
            # FIXME handle pipeline
            self.refresh_plot()
        else:
            # Disconnect observers
            self.unobserve("selected_x_axis", self._handle_selected_x_axis_changed)
            self.unobserve("selected_y_axes", self._handle_selected_x_axes_changed)
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

        self._datastore.store_data({f"sviewer/plot_1d_{self._index}/x": (new_x, None)})

    def _handle_selected_y_axes_change(self, change):
        """ """
        data = self._workspace._loader.load_data(
            change["value"],
            {m.mask_id: (m.content_id, m.value) for m in self.filters},
        )

        self._datastore.store_data(
            {
                # XXX set metadata to indicate data origin
                f"sviewer/plot_1d_{self._index}/y_{i}": (data[y_name].values, None)
                for i, y_name in enumerate(change["value"])
            }
        )

        if change["oldvalue"] and len(change["oldvalue"]) < len(change["value"]):
            pass  # XXX Add extra plots

    def _handle_filters_change(self, change):
        """Replot data when a filter parameter change."""
        self.refresh_plot()

    def _handle_file_change(self, change):
        """Event handler ensuring that we are in a consistent after a file change.

        Used to observe the workspace itself, signaling the begining of the change
        with a True and the end with a False.

        """
        # In the absence of auto refreshing there is nothing to do.
        if not self.auto_refresh:
            return

        self._post_setattr_auto_refresh(change.get("oldvalue"), change["value"])

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
                f"Got invalid position: {position}, expected 'before' or 'after'"
            )
        self.filters = filters

    def _remove_filter(self, index: int) -> None:
        """ """
        filters = self.filters[:]
        del filters[index]
        self.filters = filters


class Plot1DPanelModel(HasPreferencesAtom):
    """Model representing the current state of the 1D plots panel."""

    #: Model representing the state of each figure.
    models = List()

    #: Should any change to a parameter lead to an automatic replot.
    auto_refresh = Bool()

    #:
    # NOTE use more memory by caching intermediate results
    optimize_for_speed = Bool()

    def __init__(self, workspace, datastore):
        self.models = [Plot1DModel(i, workspace, datastore) for i in range(4)]

    def _post_setattr_auto_refresh(self, old, new):
        """"""
        if new:
            for m in self.models:
                m.enable_auto_refresh()
                m.refresh_plot()
        else:
            for m in self.models:
                m.disable_auto_refresh()

    def _post_setattr_optimize_for_speed(self, old, new):
        """"""
        # XXX clean any existing cache when disabling
        pass
