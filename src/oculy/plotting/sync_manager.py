# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Plotting plugin logic.

"""
from collections import defaultdict
from typing import Any, Mapping, MutableMapping

from atom.api import Atom, Dict, Typed
from gild.utils.atom_util import tagged_members

from oculy.data import DataStore

from .plots import BasePlot


class SyncMarker(Atom):
    """Class used to enforce some conditions are met before performing an
    update."""

    # FIXME use is unclear and as a consequence the API is to be designed
    pass


class SyncManager(Atom):
    """Manager handling updating the plot any time data change in the data
    store."""

    #: Reference to the data store
    datastore = Typed(DataStore)

    #: Plot for which some attribute need to be in sync with the data store.
    plot = Typed(BasePlot)

    #: Members to be synced and the corresponding field in data store.
    #: Members name can contain a single . to specify that an attribute of
    # the object
    #: stored in the structure should be updated. If the structure is frozen,
    # it is
    #: assumed it has a constructor able of handling member names as keyword
    # argument.
    #: This is mostly useful for things that need to be updated in a single
    # shot
    #: such as data driving a plot.
    # TODO allowing sync on metadata may be valuable for things such as units
    synced_members = Dict(str, str)

    def __init__(
        self,
        datastore: DataStore,
        plot: BasePlot,
        synced_members: Mapping[str, str],
    ):
        super().__init__(datastore=datastore, plot=plot,
                         synced_members=synced_members)
        # Ensure that all the members that are supposed to be synced
        # can be synced
        plt_sync_tag = tagged_members(plot, "sync")
        bare_sync_members = [m.split(".")[0] for m in synced_members]
        if any(m not in plt_sync_tag for m in bare_sync_members):
            raise RuntimeError(
                "Synchronization to the data store was requested for: "
                f"{list(synced_members)}. But the only members that can be"
                f" synced are "
                f"{list(plt_sync_tag)}"
            )

        self._sync_markers = {
            k: plt_sync_tag[k].metadata["sync"]
            for k in bare_sync_members
            if isinstance(plt_sync_tag[k].metadata["sync"], SyncMarker)
        }

        update_map = defaultdict(list)
        for k, v in synced_members.items():
            update_map[v].append(k)
        self._update_map = update_map

        self.datastore.observe("update", self.update_plot)

    def update_plot(self, change: Mapping[str, Any]):
        """Update the plot based on the modification to the data store."""
        if any(v in change["value"]["removed"] for v in
               self.synced_members.values()):
            self.plot.axes.remove_plot(self.plot.id)

        # Build mapping of updated values
        all_updates = change["value"]["updated"]
        updates = {k: v for k, v in self.synced_members.items() if v in
                   all_updates}
        if not updates:
            return

        data = self.datastore.get_data(updates.values())
        updates = {k: data[v].values for k, v in updates.items()}

        for k, v in updates.items():
            if k in self._sync_markers:
                raise RuntimeError("Custom sync marker are not supported.")

        batched: MutableMapping[str, MutableMapping[str, Any]] = \
            defaultdict(dict)
        for k, v in updates.items():
            if "." in k:
                obj, m = k.split(".")
                batched[obj][m] = v
            else:
                setattr(self.plot, k, v)

        for k in batched:
            old = getattr(self.plot, k)
            values = {m: getattr(old, m) for m in old.members()}
            values.update(batched[k])
            setattr(self.plot, k, type(old)(**values))

    # --- Private API

    #: Inverse mapping of the synced members allowing to quickly
    # perform the updates
    _update_map = Dict()

    #: Cache of the markers for synced members
    _sync_markers = Dict(str, SyncMarker)
