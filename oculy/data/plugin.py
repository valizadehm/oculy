# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Central data storage system for Oculy.

"""
from atom.api import Typed
from enaml.workbench.api import Plugin

# store_data(id, data, metadata) relies on typing, . separated str
# store_loader_as_dataset

from .datastore import DataStore


class DataStoragePlugin(Plugin):
    """Plugin handling storing for the whole application."""

    #: Data store object handling the book keeping.
    data = Typed(DataStore)
