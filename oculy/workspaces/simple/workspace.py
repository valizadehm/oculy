# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Simple workspace manifest.

"""
import os

import enaml
from atom.api import Bool, Dict, List, Str, Typed
from enaml.workbench.ui.api import Workspace
from glaze.utils import invoke_command
from glaze.utils.atom_util import (
    preferences_from_members,
    update_members_from_preferences,
)
from watchdog.events import (
    FileCreatedEvent,
    FileDeletedEvent,
    FileMovedEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer
from watchdog.observers.api import ObservedWatch

from oculy.data import Dataset
from oculy.io.loader import BaseLoader, BaseLoaderView

from .plot_1d_model import Plot1DPanelModel

# from .plot_2d_model import Plot2DPanelModel
with enaml.imports():
    from .content import SimpleViewerContent


class FileListUpdater(FileSystemEventHandler):
    """Watchdog event handler ensuring the list of plots is up to date."""

    def __init__(self, workspace):
        self.workspace = workspace

    def on_created(self, event):
        super(FileListUpdater, self).on_created(event)
        if isinstance(event, FileCreatedEvent):
            self.workspace._update_available_files()

    def on_deleted(self, event):
        super(FileListUpdater, self).on_deleted(event)
        if isinstance(event, FileDeletedEvent):
            self.workspace._update_available_files()

    def on_moved(self, event):
        super(FileListUpdater, self).on_deleted(event)
        if isinstance(event, FileMovedEvent):
            self.workspace._update_available_files()


class SimpleViewerWorkspace(Workspace):
    """State of the simple viewer workspace."""

    #: Currently selected folder in which to look for data.
    selected_folder = Str().tag(pref=True)

    #: List of files in the selected folder.
    available_files = List(str).tag(pref=True)

    #: Are the files filtered so as to display only files for which a loader exist.
    should_filter_files = Bool(True).tag(pref=True)

    #: Currently selected file.
    selected_file = Str().tag(pref=True)

    #: Loader ids.
    matching_loaders = List(str).tag(pref=True)

    #: Are the loader ids are filtered to match the selected file.
    should_filter_loaders = Bool(True).tag(pref=True)

    #: Id of the currently selected loader.
    selected_loader = Str().tag(pref=True)

    #: Should data be loaded automatically.
    auto_load = Bool().tag(pref=True)

    #: Flag signaling that a file change is about to happen.
    file_changing = Bool()

    #: Content of the loaded file. This dict is never updated in place and
    #: can hence be safely observed.
    file_content = Dict()

    # Set up methods used for handling preferences
    update_members_from_preferences = update_members_from_preferences
    preferences_from_members = preferences_from_members

    def start(self):
        """ """
        datastore = self.workbench.get_plugin("oculy.data").datastore
        # Create nodes used to stored data related to this workspace plots.
        datastore.store_data(
            {
                "_simple_viewer/1d": (Dataset(), None),
                "_simple_viewer/2d": (Dataset(), None),
            }
        )

        self._1d_plots = Plot1DPanelModel(self, datastore)
        # self._2d_plots = Plot2DPanelModel(self, datastore)

        self.content = SimpleViewerContent(workspace=self)

    # FIXME clean up data store
    def stop(self):
        datastore = self.workbench.get_plugin("oculy.data").datastore
        datastore.store_data({"_simple_viewer/1d": (None, None)})

        # FIXME Delete 1D and 2D plots

    def get_loader_view(self) -> BaseLoaderView:
        """Get a config view for the current loader."""
        if self._loader is None:
            self._create_loader()
        return invoke_command(
            "oculy.io.create_loader_config", self.selected_loader, self._loader
        )

    def load_file(self):
        """Create loader for selected file and determine the entries."""
        if self._loader is None:
            self._create_loader()
        self._loader.determine_content()
        self.file_changing = True
        self.content = self._loader.content
        self.file_changing = False

    # --- Private API

    #: Loader in charge of performing io for the selected file.
    _loader = Typed(BaseLoader)

    #: Watchdog observer monitoring the currently selected folder.
    _watchdog = Typed(Observer)

    #: Handler for watchdog events.
    _watchdog_handler = Typed(FileListUpdater)

    #: Watch of teh watchdog.
    _watchdog_watch = Typed(ObservedWatch)

    #: Cache of loader paarmeters used by the user in this session.
    #: Cross-session persistence should be handled through the io plugin.
    _loader_state_cache = Dict(str)

    #: State of the 1D plots
    _1d_plots = Typed(Plot1DPanelModel)

    #: State of the 2D plot
    # _2d_plots = Typed(Plot2DPanelModel)

    def _update_available_files(self):
        """Update the list of available files."""
        files = []
        trim = len(self.selected_folder) + 1
        exts = self.workbench.get_plugin("oculy.io").supported_extensions
        for dirpath, dirnames, filenames in os.walk(self.selected_folder):
            files.extend(
                sorted(
                    [
                        # Ensure we always get a full path by joining filename and
                        # selected dir
                        os.path.join(dirpath, f)[trim:]
                        for f in filenames
                        # Skip next branch if filtering is not required
                        if (not self.should_filter_files)
                        or any(f.endswith(ext) for ext in exts)
                    ]
                )
            )
        self.available_files = files
        if self.selected_file not in files:
            self.selected_file = files[0] if files else ""

    def _update_matching_loaders(self):
        """Update the list of loaders matching the selected file."""
        matching, preferred = invoke_command(
            "oculy.io.list_matching_loaders", {"filename": self.selected_file}
        )
        self.matching_loaders = matching
        if self.selected_loader not in matching:
            self.selected_loader = preferred

    def _create_loader(self):
        """Create a loader matching selection."""
        self._loader = invoke_command(
            "oculy.io.create_loader",
            {
                "id": self.selected_loader,
                "path": os.path.join(self.selected_folder, self.selected_file),
            },
        )

    def _post_setattr_selected_folder(self, old, new):
        """Ensure the available file list is up to date and remains so."""
        if self._watchdog_watch:
            self._watchdog.unschedule(self._watchdog_watch)

        self._update_available_files()

        self._watchdog_watch = self._watchdog.schedule(self._watchdog_handler, self.new)
        if not self._watchdog.isAlive():
            self._watchdog.start()

    def _post_setattr_should_filter_files(self, old, new):
        """Ensure the available file list respect filtering."""
        self._update_available_files()

    def _post_setattr_selected_file(self, old, new):
        """Ensure the loader list matches the selected file."""
        self._update_matching_loaders()
        if self._loader is not None:
            self._loader.path = os.path.join(self.selected_folder, self.selected_file)
        if self.auto_load:
            self.load_file()

    def _post_setattr_should_filter_loaders(self, old, new):
        """Ensure the matching loader list respect filtering."""
        self._update_matching_loaders()

    def _post_setattr_selected_loader(self, old, new):
        """Discard the previously created loader."""
        if self._loader:
            self._loader_state_cache[old] = self.loader.preferences_from_members()
        self._loader = None

    def _post_set_auto_load(self, old, new):
        """Ensure we auto-load the rele"""
        if new and self.selected_folder and self.selected_file and self.selected_loader:
            self.load_file()
