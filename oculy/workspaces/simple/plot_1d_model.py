# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Model driving the 1D plot panel.

"""
from atom.api import Atom, Bool, List, Str, Typed
from glaze.utils.atom_util import HasPreferencesAtom

from .mask_parameters import MaskParameter


# XXX need a clean way to handle file replacement without causing any plot crash
# use file_changing on workspace to disable update to plotswhile file is changing
# and get back to a consistent state once the change is over. The UI ensure we have
# consistent axes with respect to the new file.
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
        pass

    def run_pipeline(self):
        pass  # FIXME complete when data processing comes into play

    # --- Private API

    #: Flag signaling a file change is occuring and hence ignore UI updates
    _file_changing = Bool()

    def _update_plots(self, data: Mapping[str, Any]):
        """ """
        # XXX
        # - data need to be queried earlier to avoid re-querying things we already have
        pass

    def _post_setattr_selected_x_axis(self, old, new):
        """"""
        if self._file_changing:
            return
        # XXX Ensure that change to x axes do not break filtering/pipelines
        pass

    def _post_setattr_selected_y_axes(self, old, new):
        """ """
        if self._file_changing:
            return
        # XXX Ensure that change to y axes do not break filtering/pipelines
        pass

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

    def _remove_filter(self, index: int) -> None:
        """ """
        filters = self.filters[:]
        del filters[index]
        self.filters = filters

    def _handle_file_changed(self, change):
        """Event handler ensuring that we are in a consistent after a file change."""
        self._file_changing = change["value"]
        if not self._file_changing:
            pass  # Handle the resync (remove redundant filters )


class Plot1DPanelModel(HasPreferencesAtom):
    """Model representing the current state of the 1D plots panel."""

    #: Model representing the state of each figure.
    models = List()

    #:
    # NOTE use more memory by caching intermediate results
    optimize_for_speed = Bool()

    # XXX need to handle the use of a common x axis

    def __init__(self, workspace, datastore):
        self.models = [Plot1DModel(i, workspace, datastore) for i in range(4)]

    def _post_setattr_optimize_for_speed(self, old, new):
        """"""
        # XXX clean any existing cache when disabling
        pass
