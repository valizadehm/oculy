# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Plugin IO for Oculy.

"""
from typing import Mapping

from atom.api import Dict, Typed
from glaze.utils.plugin_tools import ExtensionsCollector, make_extension_validator
from glaze.utils.atom_util import HasPreferencesAtom
from xarray import Dataset

from oculy.transformations import MaskSpecification
from .loader import BaseLoader, Loader

LOADER_POINT = "oculy.io.loaders"


class IOPlugin(HasPreferencesAtom):
    """Plugin responsible for handling IO

    This plugin is in particular in charge of loading experimental data to be
    visualized.

    """

    #: Preferred loader for a given extension.
    preferred_loader = Dict(str, str).tag(pref=True)

    #: Custom association between loaders and file extensions.
    custom_loader_extensions = Dict().tag(pref=True)

    #: Collect all contributed Loader extensions.
    loaders = Typed(ExtensionsCollector)  # XXX make private

    def start(self) -> None:
        """Start the plugin life-cycle.

        This method is called by the framework at the appropriate time. It
        should never be called by user code.

        """
        core = self.workbench.get_plugin("enaml.workbench.core")
        core.invoke_command("exopy.app.errors.enter_error_gathering")

        validator = make_extension_validator(
            Loader, ("get_cls", "get_config_view"), ("file_extensions")
        )
        self.loaders = ExtensionsCollector(
            workbench=self.workbench,
            point=LOADER_POINT,
            ext_class=Loader,
            validate_ext=validator,
        )

        self.loaders.start()

        core.invoke_command("exopy.app.errors.exit_error_gathering")

    def stop(self) -> None:
        """Stop the plugin life-cycle.

        This method is called by the framework at the appropriate time.
        It should never be called by user code.

        """
        self.loaders.stop()
        del self.loaders

    # list_matching_loaders

    def create_loader(self, id: str, path: str) -> BaseLoader:
        """Create a loader associated with a path

        Parameters
        ----------
        id : str
            Id of the loader to create.
        path : str
            Path to the data file from which to load data.

        Returns
        -------
        BaseLoader
            BaseLoader subclass that can be used to access the file content.

        Raises
        ------
        KeyError:
            Raised if an unknown loader is requested.

        """
        if id not in self.loaders.contributions:
            # FIXME
            raise KeyError()

        # Get the loader declaration
        decl = self.loaders.contributions[id]

        def mask_data(
            to_filter: Dataset,
            filter_base: Dataset,
            specifications: Mapping[str, MaskSpecification],
        ) -> Dataset:
            # XXX should we be invoking a command here ?
            mask = self.workbench.get_plugin("oculy.transformations").create_mask(
                filter_base, specifications
            )
            return to_filter.where(mask)

        loader = decl.get_cls()(
            path=path, mask_data=mask_data, **self._loader_preferences.get(id, {})
        )

        return loader

    # --- Private API ---------------------------------------------------------

    #: Store user preferences for loaders.
    _loader_preferences = Dict().tag(pref=True)
