# ----------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# ----------------------------------------------------------------------------
"""

"""
from typing import TypeVar, Union

# Declare if the node operate in place or copy the data
# Units ? Do not need a separate declaration if we appply the pipeline on pint
# quantity but could be useful though
import numpy as np
from atom.api import Bool, Callable, Str
from enaml.core.api import Declarative, d_


# Used to declare transformation nodes
class Node(Declarative):
    """"""

    #:
    id = d_(Str())

    #:
    # Do signature analysis to determine if the workbench is necessary to the
    # node working.
    func = d_(Callable())

    #:
    operate_in_place = d_(Bool())

    #:
    # FIXME when converting diagram to script can the function call be avoided
    # FIXME inlineable node are assumed trivial and are not made available to
    # scripting
    inlineable = d_(Bool())


# --- Trivial nodes that could all be inlined
# FIXME once numpy 1.21 is out can use numpy.typing
T = TypeVar("T", bound=np.ndarray)
Index = TypeVar("Index", bound=np.ndarray)


def index_array(array: T, index: Union[int, Index]) -> T:
    return array[index]


# FIXME add logical operations, arithmetic operation, etc
