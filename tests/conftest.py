# -----------------------------------------------------------------------------
# Copyright 2022 by Oculy Authors
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# -----------------------------------------------------------------------------
"""Pytest fixtures.

"""
import os
import pathlib

import pytest
import rtoml as toml
from enaml.qt import QT_API

os.environ.setdefault("PYTEST_QT_API", QT_API)

pytest_plugins = ("gild.testing.fixtures",)


@pytest.fixture
def app_dir_storage(monkeypatch, tmpdir) -> pathlib.Path:
    """Path at which the file storing the app dir location is stored."""
    monkeypatch.setattr(pathlib.Path, "home", lambda: pathlib.Path(str(tmpdir)))
    print(pathlib.Path(str(tmpdir), ".oculy"))
    yield pathlib.Path(str(tmpdir), ".oculy")


@pytest.fixture
def app_dir(tmpdir, app_dir_storage):
    """Temporary application directory"""
    app_dir = pathlib.Path(str(tmpdir)) / "test"
    app_dir.mkdir(exist_ok=True, parents=True)
    with open(app_dir_storage, "w") as f:
        toml.dump(dict(app_path=str(app_dir)), f)

    yield app_dir

app_dir_storage