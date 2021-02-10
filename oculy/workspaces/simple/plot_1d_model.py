# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Model driving the 1D plot panel.

"""
from contextlib import contextmanager
from typing import Mapping, Iterator

import numpy as np
from atom.api import Atom, Bool, List, Str, Typed
from glaze.utils.atom_util import HasPreferencesAtom

from oculy.plotting.plots import Figure
from .mask_parameters import MaskParameter


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

    def __init__(self, index, workspace, datastore):
        # XXX Create the figure, and store the datastore.
        pass

    def refresh_plot(self) -> None:
        """Force the refreshing of the plot."""
        pass

    def enable_auto_refresh(self) -> None:
        """Connect observers to auto refresh when a plot input parameter change."""
        pass

    def disable_auto_refresh(self) -> None:
        """Disconnect observers auto refreshing when an input parameter change."""
        pass

    @contextmanager
    def ongoing_refresh(self) -> Iterator:
        """While a refresh is underway ignore external request for updates."""
        if self._auto_refresh:
            self.disable_auto_refresh()
        yield
        if self._auto_refresh:
            self.enable_auto_refresh()

    # --- Private API

    #: Reference to the figure being displayed
    _figure = Typed(Figure)

    #:
    _auto_refresh = Bool()

    def _update_plot(self, data: Mapping[str, np.ndarray]):
        """Update the plot driven by this model."""
        # XXX
        # - data need to be queried earlier to avoid re-querying things we already have
        # - need to be aware of x data sharing since

    # XXX make this an observer
    def _post_setattr_selected_x_axis(self, old, new):
        """Refresh the plot to use the new x axis."""
        # Ignore such changes during a file change since both x and y are
        # susceptible to change
        if self._file_changing:
            return

    # XXX make this an observer
    def _post_setattr_selected_y_axes(self, old, new):
        """ """
        if self._file_changing:
            return
        # XXX Ensure that change to y axes do not break filtering/pipelines
        pass

    # XXX make this an observer
    def _post_setattr_filters(self, old, new):
        """ """
        if self._file_changing:
            return
        # XXX manage observers and request replot if relevant and allowed

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
        # XXX handle auto refresh

    def _remove_filter(self, index: int) -> None:
        """ """
        filters = self.filters[:]
        del filters[index]
        self.filters = filters

    def _handle_file_change(self, change):
        """Event handler ensuring that we are in a consistent after a file change.

        Used to observe the workspace itself, signaling the begining of the change
        with a True and the end with a False.

        """
        # In the absence of auto refreshing there is nothing to do.
        if not self._auto_refresh:
            return

        if change["value"]:
            self.disable_auto_refresh()
        else:
            self.enable_auto_refresh()
            self.refresh_plot()


class Plot1DPanelModel(HasPreferencesAtom):
    """Model representing the current state of the 1D plots panel."""

    #: Model representing the state of each figure.
    models = List()

    #: Should any change to a parameter lead to an automatic replot.
    auto_refresh = Bool()

    #:
    # NOTE use more memory by caching intermediate results
    optimize_for_speed = Bool()

    # XXX need to handle the use of a common x axis

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
