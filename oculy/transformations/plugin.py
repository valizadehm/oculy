# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Logic for the data transformation plugin.

"""
from typing import Mapping

import numpy as np
from atom.api import List, Typed
from glaze.utils.atom_util import HasPrefAtom
from glaze.utils.plugin_tools import ExtensionsCollector, make_extension_validator

from .mask import Mask, MaskSpecification
from .node import Node

MASKING_POINT = "oculy.transformers.masking"

NODES_POINT = "oculy.transformers.compute_nodes"


# FIXME add proper node support (namespaced and with automatic classification
# based on signature)
class TransformerPlugin(HasPrefAtom):
    """Plugin responsible for handling data transformation including masking."""

    #: Ids of the contributed masks
    masks = List(str)

    #: Collect all contributed Node extensions.
    nodes = Typed(ExtensionsCollector)

    def start(self) -> None:
        """Start the plugin life-cycle.

        This method is called by the framework at the appropriate time. It
        should never be called by user code.

        """
        core = self.workbench.get_plugin("enaml.workbench.core")
        core.invoke_command("exopy.app.errors.enter_error_gathering")

        validator = make_extension_validator(Mask, (), ("func"))
        self._masks = ExtensionsCollector(
            workbench=self.workbench,
            point=MASKING_POINT,
            ext_class=Mask,
            validate_ext=validator,
        )
        self._masks.observe("contributions", self._update_masks)

        self._masks.start()

        validator = make_extension_validator(Node, (), ("func"))
        self._masks = ExtensionsCollector(
            workbench=self.workbench,
            point=NODES_POINT,
            ext_class=Node,
            validate_ext=validator,
        )

        self.nodes.start()

        core.invoke_command("exopy.app.errors.exit_error_gathering")

    def stop(self) -> None:
        """Stop the plugin life-cycle.

        This method is called by the framework at the appropriate time.
        It should never be called by user code.

        """
        self._masks.stop()
        del self._masks

        self.nodes.stop()
        del self.nodes

    # FIXME use numpy.typing when available
    # FIXME docstring
    def create_mask(
        self,
        filter_base: Mapping[str, np.ndarray],
        specifications: Mapping[str, MaskSpecification],
    ) -> np.ndarray:
        """[summary]

        Parameters
        ----------
        filter_base : Mapping[str, np.ndarray]
            [description]
        specifications : Mapping[str, MaskSpecification]
            [description]

        Returns
        -------
        np.ndarray
            [description]
        """
        mask = None
        for k, v in specifications.items():
            temp = self._masks[k].func(filter_base[k], *v)
            mask = mask & temp if mask is not None else temp
        return mask

    # --- Private API ---------------------------------------------------------

    #: Collect all contributed Mask extensions.
    _masks = Typed(ExtensionsCollector)

    def _update_masks(self, change):
        """Update the list of contributed masks ids."""
        self.masks = list(self._masks.contributions)
