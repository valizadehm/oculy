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
# This should be provided as extension to the plugin
class MaskParameter(Atom):
    """"""

    #: Column used as source to compute the mask
    content_id = Str()

    #: ID of the mask to apply
    mask_id = Str("==")

    #: Value used to generate the mask
    value = Float()
