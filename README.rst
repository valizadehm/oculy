Oculy: Modular data viewer
==========================

Installation
------------

Currently Oculy cannot be installed directly due to one of its dependency not
being available on PyPI. To install it directly from GitHub, you can::

    pip install git+https://github.com/MatthieuDartiailh/glaze
    pip install git+https://github.com/MatthieuDartiailh/oculy

Once installed Oculy can be started by either running::

    oculy

or::

    python -m  oculy

The second option allow you to see the program console output and can be useful to debug issues.

Build
-----
With the above in place, the package **oculy** can now be built by running::

    python -m build --wheel
from the folder where the ``pyproject.toml`` resides.
(You may need to install the build package first)::

    pip install build

This should create a ``build/`` folder as well as a ``dist/`` folder in which
one will find a wheel named something like ``oculy-0.0.0.whl``.
(don't forget to add these to your ``.gitignore``, if they aren’t in there already!)
One can install this package anywhere by copying it to the relevant machine and running::

    pip install oculy-0.0.0.whl

When developing one probably does not want to re-build and re-install the wheel
every time once they have made a change to the code, and for that one can use
an editable install::

    pip install -e .

This will install your package without packaging it into a file, but by
referring to the source directory.