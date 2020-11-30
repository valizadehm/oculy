# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Plugin IO for Oculy.

"""
from glaze.utils.atom_util import HasPreferencesAtom


class IOPlugin(HasPreferencesAtom):
    """"""

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def create_loader(self):
        pass
