# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""CSV data loader.

"""
import enaml

from .csv_loader import CSVLoader

with enaml.imports():
    from .csv_config import CSVLoaderConfig

__all__ = ("CSVLoader", "CSVLoaderConfig")
