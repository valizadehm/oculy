# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Central data storage system for Oculy.

"""
from atom.api import Dict, Event, Tuple
from enaml.workbench.api import Plugin

# store_data(id, data, metadata) relies on typing, . separated str
# store_loader_as_dataset

from .dataset import Dataset


class DataStoragePlugin(Plugin):
    """ """

    # Can be observed in a reliable manner
    entries = Tuple(str)

    #:
    entry_changed = Event()

    # --- Private API ---------------------------------------------------------

    #:
    _data = Dict(str, Dataset)
