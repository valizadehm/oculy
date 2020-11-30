# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Plugin IO for Oculy.

"""
from atom.api import Dict, Typed
from glaze.utils.plugin_tools import ExtensionsCollector, make_extension_validator
from glaze.utils.atom_util import HasPreferencesAtom

from .loader import BaseLoader, Loader

LOADER_POINT = "oculy.io.loaders"


class IOPlugin(HasPreferencesAtom):
    """Plugin responsible for handling IO

    This plugin is in particular in charge of loading experimental data to be
    visualized.

    """

    #: Custom association between loaders and file extensions.
    custom_loader_extensions = Dict()

    #: Collect all contributed Loader extensions.
    loaders = Typed(ExtensionsCollector)

    def start(self) -> None:
        """Start the plugin life-cycle.

        This method is called by the framework at the appropriate time. It
        should never be called by user code.

        """
        validator = make_extension_validator(Loader, ("get_cls"), ("file_extensions"))
        self.loaders = ExtensionsCollector(
            workbench=self.workbench,
            point=LOADER_POINT,
            ext_class=Loader,
            validate_ext=validator,
        )

        self.loaders.start()

    def stop(self) -> None:
        """Stop the plugin life-cycle.

        This method is called by the framework at the appropriate time.
        It should never be called by user code.

        """
        self.loaders.stop()
        del self.loaders

    def create_loader(self, id: str, path: str) -> BaseLoader:
        """[summary]

        Parameters
        ----------
        id : str
            [description]
        path : str
            [description]

        Returns
        -------
        BaseLoader
            [description]
        """
        pass
