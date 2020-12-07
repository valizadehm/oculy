# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""

"""
from typing import Any, Union
from atom.api import Atom, Dict, Event, ForwardInstance, Tuple

from .dataarray import DataArray


class Dataset(Atom):
    """"""

    #:
    # Can be observed in a reliable manner
    entries = Tuple(str)

    #:
    entry_changed = Event()

    #:
    metadata_entries = Tuple(str)

    def __getitem__(self, key: str) -> Union[DataArray, "Dataset"]:
        return self._data[key]

    def __setitem__(self, key: str, value: Union[DataArray, "Dataset"]) -> None:
        old = None
        if key in self._data:
            old = self._data
        self._data[key] = value

        change = {"entry": key, "new": value}
        if old is not None:
            change["old"] = old
        else:
            self.entries = tuple(self._data)
        self.entry_changed = change

    def __delitem__(self, key: str) -> None:
        old = self._data[key]
        del self._data[key]
        self.entry_changed = {"entry": key, "old": old}

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def get_metadata(self, key: str) -> Any:
        """ """
        return self._metadata[key]

    def set_metadata(self, key: str, value: Any) -> None:
        """ """
        m = self._metadata.copy()
        m[key] = value
        self._metadata = m

    _data = Dict(str, ForwardInstance(lambda: (DataArray, Dataset)))

    _metadata = Dict(str)
