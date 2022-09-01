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

Installing a development version
---------------------------------
When developing one probably does not want to re-build and re-install the wheel
every time once they have made a change to the code, and for that one can use
an editable install::

    pip install -e .

This will install your package without packaging it into a file, but by
referring to the source directory.


Generating distribution archives
---------------------------------
The next step is to generate distribution packages for the package. These are archives that are uploaded to PyPI and can
be installed by pip.
First of all, make sure you have the latest version of PyPA's build installed::

    py -m pip install --upgrade build

Now run this command from the same directory where ``pyproject.toml`` is located::

    python -m build --wheel

where ``--wheel`` flag is optional.

This should create a wheel named something like ``oculy-0.0.0-py3-none-any.whl`` in ``dist/`` folder.
One can install this install built distribution by forend tool like ``pip``.

