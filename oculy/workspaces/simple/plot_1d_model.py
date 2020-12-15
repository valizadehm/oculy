# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Model driving the 1D plot panel.

"""
from atom.api import Bool, Str, Dict
from glaze.utils.atom_util import HasPreferencesAtom


class Plot1DModel(HasPreferencesAtom):
    """ """

    #: Selected entry of the data to use as x axis.
    selected_x_axis = Str()

    #: Entries to use on y axis of each plot.
    selected_y_axes = Dict(str, list)

    #: Filtering specifications
    filtering = Dict(str, tuple)

    #:
    # NOTE use more memory by caching intermediate results
    optimize_for_speed = Bool()

    #:
    # NOTE for the time being enforce a single pipeline applied to all axis
    # Anything else would represent a UX nightmare anyway.
    pipeline = None

    def run_pipeline(self, change=None):
        pass