# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Central data storage system for Oculy.

"""
from typing import Any, Union

import numpy as np
from atom.api import Typed
from enaml.workbench.api import Plugin

from .datastore import DataStore, DataArray, Dataset


class DataStoragePlugin(Plugin):
    """Plugin handling storing for the whole application."""

    #: Data store object handling the book keeping.
    data = Typed(DataStore)

    #: Converters used to turn input data into valid data for the datastore.
    converters = None  # FIXME

    def start(self):
        pass

    def stop(self):
        pass

    def run_converters(self, data: Any) -> Union[Dataset, DataArray]:
        """Convert data to an admissible element of the data store."""
        if not isinstance(data, np.ndarray) or data.dtype.names is not None:
            # FIXME run custom converters (including for numpy arrays)
            raise NotImplementedError

        return DataArray(data=data)
