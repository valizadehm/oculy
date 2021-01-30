# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Plotting plugin logic.

"""
from typing import Any, Mapping

from atom.api import Atom, Dict, Typed
from glaze.utils.atom_utils import tagged_members

from oculy.data import DataStore
from .plots import BasePlot

# XXX work on datastore and update logic for the new central architecture.


class SyncMarker(Atom):
    """Class used to enforce some conditions are met before performing an update."""

    # XXX use is unclear and as a consequence the API is to be designed


# XXX handle data.x syntax
class SyncManager(Atom):
    """Manager handling updating the plot any time data change in the data store."""

    #: Reference to the data store
    data_store = Typed(DataStore)

    #: Plot for which some attribute need to be in sync with the data store.
    plot = Typed(BasePlot)

    #: Members to be synced and the corresponding field in data store
    synced_members = Dict(str, str)

    def __init__(
        self,
        data_plugin: DataStore,
        plot: BasePlot,
        synced_members: Mapping[str, str],
    ):
        super().__init__(
            data_plugin=data_plugin, plot=plot, synced_members=synced_members
        )
        # Ensure that all the members that are supposed to be synced can be synced
        plt_sync_tag = tagged_members(plot, "sync")
        if any(m not in plt_sync_tag for m in synced_members):
            raise RuntimeError(
                "Synchronization to the data store was requested for: "
                f"{list(synced_members)}. But the only members that can be synced are "
                f"{list(plt_sync_tag)}"
            )

        self._sync_markers = {
            k: plt_sync_tag[k].metadata["sync"]
            for k in synced_members
            if isinstance(plt_sync_tag[k], SyncMarker)
        }

        # XXX connect to the data store unique event

    def update_plot(self, change: Mapping[str, Any]):
        """Update the plot if the sync marker invariants are upheld.

        Otherwise we set up a future warning logging. That will be discarded if
        a new valid update comes before the time.

        """
        if any(v in change["value"]["removed"] for v in self.synced_members.values()):
            self.plot.axes.remove_plot(self.plot.id)

        # Build mapping of updated values
        all_updates = change["value"]["updated"]
        updates = {
            k: all_updates[v]
            for k, v in self.synced_members.items()
            if v in all_updates
        }
        if not updates:
            return

        for k, v in updates.items():
            if k in self._sync_markers:
                raise RuntimeError("Custom sync marker are not supported.")

        self.plot.update_many(updates)

    # --- Private API

    #: Cache of the markers for synced members
    _sync_markers = Dict(str, SyncMarker)
