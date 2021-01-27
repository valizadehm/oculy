# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Plotting plugin logic.

"""
from typing import Mapping

from enaml.workbench.api import Plugin

from .plots.figure import GridPosition


class PlottingPlugin(Plugin):
    """"""

    def create_figure(
        self, id: str, axes_specification: Mapping[str, GridPosition] = None
    ):
        pass

    def add_plot(self):
        pass
