# -----------------------------------------------------------------------------
# Copyright 2022 by Gild Authors
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# -----------------------------------------------------------------------------
"""Test application startup script.

"""
import pytest
from pkg_resources import EntryPoint

from oculy.__main__ import main
from gild.testing.util import handle_dialog


def test_running_main_error_in_loading(gild_qtbot, monkeypatch):
    """Test starting the main app but encountering an error while loading modifier.

    """
    import gild.utils.argparse as em

    def false_iter(arg):

        class FalseEntryPoint(EntryPoint):
            def load(self, *args, **kwargs):
                raise Exception("Can't load entry point")

        return [FalseEntryPoint('dummy', 'dummy')]

    monkeypatch.setattr(em, 'iter_entry_points', false_iter)

    def check_dialog(qtbot, dial):
        assert 'extension' in dial.text

    with pytest.raises(SystemExit):
        with handle_dialog(gild_qtbot, 'reject', check_dialog):
            main([])


def test_running_main_error_in_parser_modifying(gild_qtbot, monkeypatch):
    """Test starting the main app but encountering an issue while adding
    arguments.

    """
    import gild.utils.argparse as em

    def false_iter(arg):

        class FalseEntryPoint(EntryPoint):
            def load(self, *args, **kwargs):

                def false_modifier(parser):
                    raise Exception('Failed to add stupid argument to parser')

                return (false_modifier, 1)

        return [FalseEntryPoint('dummy', 'dummy')]

    monkeypatch.setattr(em, 'iter_entry_points', false_iter)

    def check_dialog(gild_qtbot, dial):
        assert 'modifying' in dial.text

    with pytest.raises(SystemExit):
        with handle_dialog(gild_qtbot, 'reject', check_dialog):
            main([])


def test_running_main_error_in_parsing(gild_qtbot):
    """Test starting the main app but encountering an issue while adding
    arguments.

    """
    def check_dialog(qtbot, dial):
        assert 'cmd' in dial.text

    with pytest.raises(SystemExit):
        with handle_dialog(gild_qtbot, 'reject', check_dialog):
            main(['dummy'])


def test_running_main_error_in_app_startup(gild_qtbot, monkeypatch):
    """Test starting the main app but encountering an issue when running
    startups.

    """
    from gild.plugins.lifecycle.plugin import LifecyclePlugin

    def false_run_startup(self, args):
        raise Exception('Fail to run start up')

    monkeypatch.setattr(LifecyclePlugin, 'run_app_startup', false_run_startup)

    def check_dialog(qtbot, dial):
        assert 'starting' in dial.text

    with pytest.raises(SystemExit):
        with handle_dialog(gild_qtbot, 'reject', check_dialog):
            main([])


def test_running_main(gild_qtbot, app_dir, monkeypatch):
    """Test starting the main app and closing it.

    """
    from enaml.workbench.ui.ui_plugin import UIPlugin

    def wait_for_window(self):
        pass

    # Do not release the application
    def no_release(self):
        pass

    monkeypatch.setattr(UIPlugin, '_release_application', no_release)
    monkeypatch.setattr(UIPlugin, 'start_application', wait_for_window)

    import sys
    old = sys.excepthook
    try:
        main([])
    finally:
        sys.excepthook = old


def test_running_main_asking_for_help(gild_qtbot):
    """Test starting the main app and closing it.

    """
    try:
        main(['-h'])
        # TODO make sure no window was opened ?
    except SystemExit as e:
        assert e.args == (0,)
