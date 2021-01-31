# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Central data storage system for Oculy.

"""
from typing import Union, Mapping, Any, Optional, Iterator, Tuple, Sequence

import numpy as np
from atom.api import (
    Atom,
    Bool,
    Dict,
    Event,
    ForwardInstance,
    ForwardTyped,
    Instance,
    Typed,
)

from oculy.io import BaseLoader

# XXX will have to formalize sync mechanism ...


def _plugin():
    from .plugin import DataStoragePlugin

    return DataStoragePlugin


class DataArray(Atom):
    """Leaf in the datastore, storing a read-only numpy array and custom metadata."""

    #: Values being stored, this is not meant to be a record array.
    values = Typed(np.ndarray)

    #: Is that array updated each time any of its sources are updated.
    is_live = Bool()

    #: Metadata attached to data.
    metadata = Dict(str)

    # --- Private API

    def _post_setattr_values(self, old, new):
        """Enforce that all arrays stored in the datastore are read-only."""
        new.writable = False


class Dataset(Atom):
    """Represent a node in the data store."""

    #: Custom metadata attached to the node.
    metadata = Dict(str)

    def __getitem__(self, key: str) -> Union[DataArray, "Dataset"]:
        return self._data[key]

    def __contains__(self, key: str) -> bool:
        return key in self._data

    _data = Dict(str, ForwardInstance(lambda: (DataArray, Dataset)))


# XXX TODO
# Centralizing manipulations at the datastore level will help performing
# batch updates which will prevent getting inconsistent states in plots
# All manipulations should occurs through the datastore
# Array stored in the datastored should be marked as readonly (writable=False)
# Also keep data loaders in there


class DataStore(Atom):
    """Central data storage object ensuring proper updates are provided.

    Data are stored in a hierarchical manner. Ids take the form of / separated str.

    """

    #: Live loaders stored for further access.
    loaders = Dict(str, BaseLoader)

    #: Event notifying of any change in the store. The content is a dictionary
    #: with the following keys:
    #: - "added": list of new entries.
    #: - "removed": list of entries that disappeared from the store.
    #: - "moved": dict of entries that moved from key to value.
    #: - "updated": dict of entries whose values where updated and their new value.
    #: - "metadata_updated": list of entries whose metadata values were updated.
    update = Event()

    def get_data(self, paths: Sequence[str], include_metadata: bool = False):
        """"""
        pass

    def store_data(
        self, datas: Mapping[str, Any], metadata: Optional[Mapping[str, Any]]
    ):
        """"""
        pass

    def move_data(self, move: Mapping[str, str]):
        """"""
        pass

    def copy_data(self, datas: Mapping[str, str]):
        """"""
        pass

    def create_live_data(self, pipeline, inputs, output_ids):
        """"""
        raise NotImplementedError

    def walk(self) -> Iterator[Tuple[str, Tuple[str, ...], Tuple[str, ...]]]:
        """Walk the content of the data store.

        Similar to os.walk yield: root, datasets, dataarrays

        """
        pass

    # --- Private API

    #: Reference to the plugin used to access converters.
    _plugin = ForwardTyped(_plugin)

    #: Mapping storing the data sets
    _data = Dict(str, Instance((Dataset, DataArray)))
