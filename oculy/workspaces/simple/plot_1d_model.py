# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Model driving the 1D plot panel.

"""
from atom.api import Atom, Bool, List, Str, Typed
from glaze.utils.atom_util import HasPreferencesAtom

from .mask_parameters import MaskParameter


# XXX need one structure per plot otherwise will be a nightmare to drive the UI
class Plot1DModel(Atom):
    """ """

    #: Selected entry of the data to use as x axis for each plot.
    selected_x_axis = Str()

    #: Entries to use on y axis of each plot.
    selected_y_axes = List()

    #: Filtering specifications per graph.
    filters = List(MaskParameter)

    #:
    # Allow one pipeline per graph (use a notebook on the UI side)
    pipeline = Typed()  # XXX need a dedicated container

    def run_pipeline(self):
        pass

    def _post_setattr_selected_x_axes(self, old, new):
        """ """
        # XXX Ensure that change to x axes do not break filtering/pipelines
        pass

    def _post_setattr_selected_y_axes(self, old, new):
        """ """
        # XXX Ensure that change to y axes do not break filtering/pipelines
        pass

    def _post_setattr_filters(self, old, new):
        """ """
        # XXX manage observers and request replot if relevant and allowed

    def _add_filter(self, index: int, position: str) -> None:
        """ """
        filters = self.filters[:]
        if position == "before":
            filters.insert(index, MaskParameter())
        elif position == "after":
            if index + 1 == len(filters):
                filters.append(MaskParameter())
            else:
                filters.insert(index + 1, MaskParameter())
        else:
            raise ValueError(
                f"Got invalid position: {position}, expected 'before' or 'after'"
            )
        self.filters = filters

    def _remove_filter(self, index: int) -> None:
        """ """
        filters = self.filters[:]
        del filters[index]
        self.filters = filters


class Plot1DPanelModel(HasPreferencesAtom):
    """ """

    #: Selected entry of the data to use as x axis for each plot.
    models = List(default=[Plot1DModel(), Plot1DModel(), Plot1DModel(), Plot1DModel()])

    #:
    # NOTE use more memory by caching intermediate results
    optimize_for_speed = Bool()

    def _post_setattr_optimize_for_speed(self, old, new):
        """"""
        # XXX clean any existing cache when disabling
        pass
