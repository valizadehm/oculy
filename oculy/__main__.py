# --------------------------------------------------------------------------------------
# Copyright 2020 by Oculy Authors, see git history for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# --------------------------------------------------------------------------------------
"""Application startup script.

"""
import sys
import threading
from traceback import format_exc

import enaml
from enaml.qt.qt_application import QtApplication
from enaml.workbench.api import Workbench
from glaze.utils.argparse import ArgParser, extend_parser

with enaml.imports():
    from enaml.stdlib.message_box import MessageBox, DialogButton
    from enaml.workbench.core.core_manifest import CoreManifest
    from enaml.workbench.ui.ui_manifest import UIManifest
    from glaze.plugins.lifecycle.manifest import LifecycleManifest
    from glaze.plugins.preferences.manifest import PreferencesManifest
    from glaze.plugins.states.manifest import StateManifest
    from glaze.plugins.errors.manifest import ErrorsManifest
    from glaze.plugins.icons.manifest import IconManagerManifest
    from glaze.plugins.packages.manifest import PackagesManifest
    from glaze.plugins.log.manifest import LogManifest


def setup_thread_excepthook():
    """
    Workaround for `sys.excepthook` thread bug from:
    http://bugs.python.org/issue1230540

    Call once from the main thread before creating any threads.
    """

    init_original = threading.Thread.__init__

    def init(self, *args, **kwargs):
        """Modify the run method to use sys.excepthook."""
        init_original(self, *args, **kwargs)
        run_original = self.run

        def run_with_except_hook(*args2, **kwargs2):
            """Call sys.excepthook if any error occurs in the thread."""
            try:
                run_original(*args2, **kwargs2)
            except Exception:  # pragma: no cover
                sys.excepthook(*sys.exc_info())  # pragma: no cover

        self.run = run_with_except_hook

    threading.Thread.__init__ = init


def display_startup_error_dialog(text, content, details=""):
    """Show a nice dialog showing to the user what went wrong during
    start up.

    """
    if not QtApplication.instance():
        QtApplication()  # pragma: no cover
    dial = MessageBox()
    dial = MessageBox(
        title="Oculy failed to start",
        text=text,
        content=content,
        details=details,
        buttons=[DialogButton(str("Close"), str("reject"))],
    )
    dial.exec_()
    sys.exit(1)


def main(cmd_line_args=None):
    """Main entry point of the Oculy application."""
    # Build parser from ArgParser and parse arguments
    parser = ArgParser()
    parser.add_choice("workspaces", "exopy.measurement.workspace", "measurement")
    parser.add_argument(
        "-s", "--nocapture", help="Don't capture stdout/stderr", action="store_true"
    )
    parser.add_argument(
        "-w",
        "--workspace",
        help="Select start-up workspace",
        default="single",
        choices="workspaces",
    )
    parser.add_argument(
        "-r",
        "--reset-app-folder",
        help="Reset the application startup folder.",
        action="store_true",
    )

    extend_parser(
        parser,
        "oculy_cmdline_args",
        lambda title, content, details, exception: display_startup_error_dialog(
            title, content, details
        ),
    )

    try:
        args = parser.parse_args(cmd_line_args)
    except BaseException as e:
        if e.args == (0,):
            sys.exit(0)
        text = "Failed to parse cmd line arguments"
        content = (
            "The following error occurred when trying to parse the "
            "command line arguments :\n {}".format(e)
        )
        details = format_exc()
        display_startup_error_dialog(text, content, details)

    # Patch Thread to use sys.excepthook
    setup_thread_excepthook()

    workbench = Workbench()
    workbench.register(CoreManifest())
    workbench.register(UIManifest())
    workbench.register(LifecycleManifest())
    workbench.register(StateManifest())
    workbench.register(ErrorsManifest())
    workbench.register(PreferencesManifest())
    workbench.register(IconManagerManifest())
    workbench.register(LogManifest())
    workbench.register(PackagesManifest())

    ui = workbench.get_plugin(u"enaml.workbench.ui")  # Create the application

    try:
        app = workbench.get_plugin("glaze.lifecyle")
        app.run_app_startup(args)
    except Exception as e:
        text = "Error starting plugins"
        content = (
            "The following error occurred when executing plugins "
            "application start ups :\n {}".format(e)
        )
        details = format_exc()
        display_startup_error_dialog(text, content, details)

    core = workbench.get_plugin("enaml.workbench.core")

    # Install global except hook.
    if not args.nocapture:
        core.invoke_command("glaze.errors.install_excepthook", {})

    # Select workspace
    core.invoke_command(
        "enaml.workbench.ui.select_workspace", {"workspace": args.workspace}, workbench
    )

    ui = workbench.get_plugin(u"enaml.workbench.ui")
    ui.show_window()
    ui.window.maximize()
    ui.start_application()

    core.invoke_command("enaml.workbench.ui.close_workspace", {}, workbench)

    # Unregister all contributed packages
    workbench.unregister("glaze.packages")
    workbench.unregister("glaze.icons")
    workbench.unregister("glaze.preferences")
    workbench.unregister("glaze.states")
    workbench.unregister("glaze.errors")
    workbench.unregister("glaze.logging")
    workbench.unregister("glaze.lifecyle")
    workbench.unregister("enaml.workbench.ui")
    workbench.unregister("enaml.workbench.core")


if __name__ == "__main__":

    main()  # pragma: no cover
