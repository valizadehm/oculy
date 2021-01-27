# --------------------------------------------------------------------------------------
# Copyright 2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""
"""


class Plot1DLineProxy(Plot1DProxy):
    @mark_backend_unsupported
    def set_line_weigth(self, weight: int):
        pass

    @mark_backend_unsupported
    def set_marker_size(self, size: int):
        pass

    @mark_backend_unsupported
    def set_marker_state(self, state: bool):
        pass


class Plot1DHistogramProxy(Plot1DProxy):
    pass