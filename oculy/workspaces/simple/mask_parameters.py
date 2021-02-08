# --------------------------------------------------------------------------------------
# Copyright 2020-2021 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Model describing the parameters for a mask.

"""
from atom.api import Atom, Float, Str


# FIXME this is not generic
class MaskParameter(Atom):
    """"""

    #:
    content_id = Str()

    #:
    mask_id = Str()

    #:
    value = Float()
