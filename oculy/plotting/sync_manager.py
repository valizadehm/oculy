# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Plotting plugin logic.

"""
import logging
from functools import partialmethod
from typing import Any, Mapping, Optional, Tuple

import numpy as np
from atom.api import Atom, Bool, Dict, Str, Typed, Tuple as ATuple
from enaml.application import deferred_call
from glaze.utils.atom_utils import tagged_members

from oculy.data.plugin import DataStoragePlugin
from .plots import BasePlot

# XXX work on datastore and update logic for the new central architecture.


class SyncMarker(Atom):
    """Class used to enforce some conditions are met before performing an update."""

    def check_matching(
        self,
        object: Atom,
        tagged_values: Any
    ) -> Tuple[bool, str]:
        """Check a value against the values store on an object.

        Parameters
        ----------
        object : Atom
            Object on which the tagged and matching attributes exist
        tagged_value : Any
            Value of the tagged member to check for conformity.

        Returns
        -------
        bool
            Was the check successful
        str
            Error message to be emitted if the check fails.

        """
        return True, ""


class ShapeMatchingMarker(SyncMarker):
    """Enforce matching between the shape of the tagged attribute and other attributes."""

    #: Name of the other attributes
    matching_attributes = ATuple(str)

    def check_matching(
        self,
        object: Atom,
        tagged_value: np.ndarray, # XXX update
    ) -> Tuple[bool, str]:
        """Check a value against the values store on an object.

        Parameters
        ----------
        object : Atom
            Object on which the tagged and matching attributes exist
        tagged_value : np.ndarray
            Value of the tagged member to check for conformity.
        pending_values : Mapping[str, np.ndarray]
            Previous updates that did not go through.

        Returns
        -------
        bool
            Was the check successful
        str
            Error message to be emitted if the check fails.

        """
        mismatching = [
            (
                m,
                getattr(object, m).shape
                if m not in pending_values
                else pending_values[m],
            )
            for m in self.matching_attributes
            if tagged_value.shape != getattr(object, m).shape
        ]
        if mismatching:
            return (
                False,
                f"Shape {tagged_value.shape} does not match shape of {mismatching}",
            )

        return True, ""


class SyncManager(Atom):
    """Manager handling updating the plot any time data change in the data store."""

    #: Reference to the data plugin
    data_plugin = Typed(DataStoragePlugin)

    #: Plot for which some attribute need to be in sync with the data store.
    plot = Typed(BasePlot)

    #: Members to be synced and the corresponding field in data store
    synced_members = Dict(str, str)

    def __init__(
        self,
        data_plugin: DataStoragePlugin,
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

        for m, data_store_path in synced_members.items():
            # NOTE this should probably be abstracted away in the data store
            data = data_plugin.data
            for part in data_store_path.split("/"):
                if hasattr(data, "entry_updated"):
                    # We are dealing with a dataset
                    data.observe(
                        "entry_updated", partialmethod(self.handle_store_change, m)
                    )
                else:
                    # We are dealing with a data array
                    data.observe("values_changed", partialmethod(self.update_plot, m))

        # XXX set up all the required observers (on the dataarrays and on the datasets)
        # Enforce shape matching based on member annotation and silence updates
        # leading to shape mismatch

    def update_plot(self, member_name, change: Mapping[str, Any]):
        """Update the plot if the sync marker invariants are upheld.

        Otherwise we set up a future warning logging. That will be discarded if
        a new valid update comes before the time.

        """
        sync = getattr(self.plot, member_name).metadata["sync"]
        if isinstance(sync, SyncMarker):
            state, msg = sync.check_matching(
                self.plot, change["value"], self._pending_values
            )
        else:
            state, msg = True, ""

        if state:
            # In the presence of pending values we update those while suppressing
            # notifications and then update the new value, assuming that this will
            # be sufficient to propagate the update.
            if self._pending_values:
                with self.plot.suppress_notifications():
                    for k, v in self._pending_values.items():
                        setattr(self.plot, k, v)
                    setattr(self.plot, member_name, change["value"])
                self.plot.
            else:
                pass
        else:

            timed_call(
                1000,
            )

    # --- Private API

    #: Updates that could not go through due to a mismatch.
    _pending_values = Dict(str, np.ndarray)

    #: Future warning that can be emitted if unmatching updates are not cancelled
    #: by following updates.
    _future = Typed(DelayedWarning)
