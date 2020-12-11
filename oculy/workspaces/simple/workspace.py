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

from atom.api import Bool, List, Str, Typed
from enaml.workbench.ui.api import Workspace
from glaze.utils import invoke_command
from watchdog.events import (
    FileCreatedEvent,
    FileDeletedEvent,
    FileMovedEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer
from watchdog.observers.api import ObservedWatch

from oculy.data import Dataset
from oculy.io.loader import BaseLoader


class FileListUpdater(FileSystemEventHandler):
    """"""

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
    """"""

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

    def start(self):
        """ """
        data = invoke_command(self.workbench, "glaze.state.get_state", "oculy.data")
        self._dataset = data["_simple_viewer"] = Dataset()

        # XXX Create 1D and 2D plots

    # FIXME clean up data store
    def stop(self):
        data = invoke_command(self.workbench, "glaze.state.get_state", "oculy.data")
        del data["_simple_viewer"]

        # XXX Delete 1D and 2D plots

    def get_loader_view(self):
        """ """
        pass

    def load_file(self):
        """ """
        pass

    # --- Private API

    #: Dataset driving the plots of the 1D and 2D panels.
    _dataset = Typed(Dataset)

    #: Loader in charge of performing io for the selected file.
    _loader = Typed(BaseLoader)

    #: Watchdog observer monitoring the currently selected folder.
    _watchdog = Typed(Observer)

    #: Handler for watchdog events.
    _watchdog_handler = Typed(FileListUpdater)

    #: Watch of teh watchdog.
    _watchdog_watch = Typed(ObservedWatch)

    #:
    _io_state = Typed()  # XXX

    def _update_available_files(self):
        """Update the list of available files."""
        files = []
        trim = len(self.selected_folder) + 1
        exts = self._io_state.supported_extensions
        for dirpath, dirnames, filenames in os.walk(self.selected_folder):
            files.extend(
                sorted(
                    [
                        # Ensure we always get a full path by joining filename and
                        # selected dir
                        os.path.join(dirpath, f)[trim:]
                        for f in filenames
                        # skip next branch if filtering is not required
                        if (not self.should_filter_files)
                        or any(f.endswith(ext) for ext in exts)
                    ]
                )
            )
        self.available_files = files
        if self.selected_file not in files:
            self.selected_file = files[0] if files else ""

    def _update_matching_loaders(self):
        """"""
        matching, preferred = invoke_command(
            "oculy.io.list_matching_loaders", {"filename": self.selected_file}
        )
        self.matching_loaders = matching
        if self.selected_loader not in matching:
            self.selected_loader = preferred

    def _post_set_selected_folder(self, old, new):
        """Ensure the available file list is up to date and remains so."""
        if self._watchdog_watch:
            self._watchdog.unschedule(self._watchdog_watch)

        self._update_available_files()

        self._watchdog_watch = self._watchdog.schedule(self._watchdog_handler, self.new)
        if not self._watchdog.isAlive():
            self._watchdog.start()

    def _post_set_should_filter_files(self, old, new):
        """Ensure the available file list respect filtering."""
        self._update_available_files()

    def _post_set_selected_file(self, old, new):
        """Ensure the loader list matches the selected file."""
        self._update_matching_loaders()
        if self.auto_load:
            self.load_file()

    def _post_set_should_filter_loaders(self, old, new):
        """Ensure the matching loader list respect filtering."""
        self._update_matching_loaders()

    def _post_set_auto_load(self, old, new):
        """ """
        if new:
            self.load_file()
