# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Central data storage system for Oculy.

"""
from typing import Union

import numpy as np
from atom.api import Atom, Dict, ForwardInstance, Typed


class DataArray(Atom):
    """Leaf in the datastore, storing a read-only numpy array and custom metadata."""

    #: Values being stored, this is not meant to be a record array.
    values = Typed(np.ndarray)

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

    def __setitem__(self, key: str, value: Union[DataArray, "Dataset"]) -> None:
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __contains__(self, key: str) -> bool:
        return key in self._data

    _data = Dict(str, ForwardInstance(lambda: (DataArray, Dataset)))


# Centralizing manipulations at the datastore level will help performing
# batch updates which will prevent getting inconsistent states in plots
# All manipulations should occurs through the datastore
# Array stored in the datastored should be marked as readonly (writable=False)
# Also keep data loaders in there