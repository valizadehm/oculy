# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Data transformation plugin for Oculy.

"""
from typing import Any, Tuple

#: Description of a masking operation. Used in particular for loaders. The first
#: str should refer to the ids of a Mask contributed to the transformation plugin.
MaskSpecification = Tuple[str, Tuple[Any, ...]]
