# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Central data storage system for Oculy.

"""
from collections import deque
from typing import Any
from typing import Dict as TDict
from typing import Iterator, Mapping, Optional, Sequence, Tuple, Union

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


def _plugin():
    from .plugin import DataStoragePlugin

    return DataStoragePlugin


class DataArray(Atom):
    """
    Leaf in the datastore, storing a read-only numpy array and custom metadata.
    """

    #: Values being stored, this is not meant to be a record array.
    values = Typed(np.ndarray)

    #: Is that array updated each time any of its sources are updated.
    is_live = Bool()

    #: Metadata attached to data.
    metadata = Dict(str)

    # --- Private API

    def _post_setattr_values(self, old, new):
        """Enforce that all arrays stored in the datastore are read-only."""
        new.flags.writeable = False


class Dataset(Atom):
    """Represent a node in the data store."""

    #: Custom metadata attached to the node.
    metadata = Dict(str)

    def __getitem__(self, key: str) -> Union[DataArray, "Dataset"]:
        return self._data[key]

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def values(self) -> Iterator[Union[DataArray, "Dataset"]]:
        """Iterable on the values stored."""
        return iter(self._data.values())

    def items(self) -> Iterator[Tuple[str, Union[DataArray, "Dataset"]]]:
        """Iterable on the keys and values stored."""
        return iter(self._data.items())

    _data = Dict(str, ForwardInstance(lambda: (DataArray, Dataset)))


def _lookup_in_store(node: Dataset, split_path: Sequence[str]):
    """Look up a node based on a list of names."""
    for k in split_path:
        node = node[k]
    return node


class DataStore(Atom):
    """
    Central data storage object ensuring proper updates are provided.

    Data are stored in a hierarchical manner. Ids take the form of /
     separated str.

    """

    #: Live loaders stored for further access.
    loaders = Dict(str, BaseLoader)

    #: Event notifying of any change in the store. The content is a dictionary
    #: with the following keys:
    #: - "added": list of new entries.
    #: - "removed": list of entries that disappeared from the store.
    #: - "moved": dict of entries that moved from key to value.
    #: - "updated": dict of entries whose values where updated and their new \
    # value.
    #: - "metadata_updated": list of entries whose metadata values were \
    # updated.
    update = Event()

    def get_data(self, paths: Sequence[str]) -> TDict[
        str, Union[Dataset, DataArray]
    ]:
        """Retrieve data as Dataset and DataArray."""
        split_paths = [path.split("/") for path in paths]
        s1 = min(split_paths)
        s2 = max(split_paths)
        common = s1
        for i, c in enumerate(s1):
            if c != s2[i]:
                common = s1[:i]
                break

        data = {}
        root = _lookup_in_store(self._data, common)
        for p, sp in zip(paths, split_paths):
            data[p] = _lookup_in_store(root, sp[len(common):])

        return data

    def store_data(
        self, data: Mapping[str, Tuple[
                Optional[Any], Optional[Mapping[str, Any]]
            ]]
    ) -> None:
        """Store data in the store.

        All intermediate node are create automatically, and metadata are
        updated based on the provided values. Metadata with None as value
        are deleted, and entry with None for both values and metadat are
        removed.

        The converters declared in the plugin are used to turn the provided
        values into admissible values for the data member of a DataArray.

        Parameters
        ----------
        data : Mapping[str, Tuple[Optional[Any], Optional[Mapping[str, Any]]]]
            Mapping between path and pairs of value, metadata to store.

        """
        added = []
        updated = []
        meta_updated = []
        removed = []
        # Sort the path to ensure we always create a parent node
        # before its children
        for path in sorted(data):
            val, mval = data[path]
            current = self._data
            current_path = ""
            split_path = path.split("/")
            for p in split_path[:-1]:
                if p not in current:
                    n_path = current_path + "/" + p if current_path else p
                    current[p] = Dataset()
                    added.append(n_path)

                current = current[p]._data
                current_path += "/" + p if current_path else p

            d_key = split_path[-1]
            current_path += "/" + d_key
            if d_key not in current:
                added.append(current_path)
            else:
                if val is not None:
                    updated.append(current_path)
                if mval is not None:
                    meta_updated.append(current_path)

            if val is not None:
                if isinstance(val, (Dataset, DataArray)):
                    current[d_key] = val
                else:
                    # Call the plugin to run custom converter on the data
                    current[d_key] = self._plugin.run_converter(val)

            if mval is not None:
                current[d_key].metadata.update(mval)
                current[d_key].metadata = {
                    k: v for k, v in current[d_key].metadata.items() if v
                }

            if val is None and mval is None:
                removed.append(current_path)

        update = {}
        for k, v in zip(
            ("added", "removed", "updated", "metadata_updated"),
            (added, removed, updated, meta_updated),
        ):
            update[k] = v

        self.update = update

    def move_data(self, move: Mapping[str, str]):
        """Move data from one place to another."""
        raise NotImplementedError  # FIXME

    def copy_data(self, datas: Mapping[str, str]):
        """Copy data from one place to another."""
        raise NotImplementedError  # FIXME

    def create_live_data(self, pipeline, inputs, output_ids):
        """"""
        raise NotImplementedError

    def walk(
        self,
    ) -> Iterator[
        Tuple[
            Union["DataStore", Dataset, DataArray],
            Tuple[Tuple[str, Dataset], ...],
            Tuple[Tuple[str, DataArray], ...],
        ]
    ]:
        """Walk the content of the data store.

        Similar to os.walk yield: root, datasets, dataarrays

        """
        sets = deque([(k, v) for k, v in self._data.items() if
                      isinstance(v, Dataset)])
        arrays = tuple(
            (k, v) for k, v in self._data._values() if
            isinstance(v, DataArray)
        )
        yield self, tuple(sets), arrays

        while sets:
            for _, s in tuple(sets):
                sets.popleft()
                sets.extend([(k, v) for k, v in s.items() if
                             isinstance(v, Dataset)])
                arrays = tuple((k, v) for k, v in s.items() if
                               isinstance(v, DataArray))
                yield s, sets[-1], arrays

    # --- Private API

    #: Reference to the plugin used to access converters.
    _plugin = ForwardTyped(_plugin)

    #: Mapping storing the data sets
    _data = Dict(str, Instance((Dataset, DataArray)))
