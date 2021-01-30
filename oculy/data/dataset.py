# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""

"""
from typing import Union
from atom.api import Atom, Dict, ForwardInstance, Tuple

from .dataarray import DataArray


class Dataset(Atom):
    """"""

    #:
    entries = Tuple(str)

    #:
    metadata = Dict(str)

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

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __contains__(self, key: str) -> bool:
        return key in self._data

    _data = Dict(str, ForwardInstance(lambda: (DataArray, Dataset)))
