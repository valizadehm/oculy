# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""

"""
from contextlib import contextmanager
from typing import Iterator

import numpy as np
from atom.api import Atom, Dict, Event, Typed


class DataArray(Atom):
    """"""

    #:
    values_changed = Event()

    #:
    metadata = Dict(str)

    @contextmanager
    def values(self, read_only_use=False) -> Iterator[np.ndarray]:
        """"""
        yield self._values
        if not read_only_use:
            self.values_changed = self._values

    def set_values(self, values: np.ndarray) -> None:
        """ """
        self._values = values
        self.values_changed = values

    #:
    _values = Typed(np.ndarray)
