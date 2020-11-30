# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Simple workspace manifest.

"""
from enaml.workbench.ui.api import Workspace


class SimpleViewerWorkspace(Workspace):
    """"""

    def start(self):
        pass

    # FIXME clean up data store
    def stop(self):
        pass
