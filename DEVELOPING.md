## Development

```
mkvirtualenv pylibdmtx
pip install -U pip
pip install -r requirements.pip

nosetests
python -m pylibdmtx.scripts.read_datamatrix pylibdmtx/tests/datamatrix.png
```

### Testing python versions

Make a virtual env and install `tox`

```
mkvirtualenv tox
pip install tox
```

If you use non-standard locations for your Python builds, make the interpreters available on the `PATH` before running `tox`.

```
PATH=~/local/python-2.7.12/bin:~/local/python-3.4.5/bin:~/local/python-3.5.2/bin:$PATH
tox
```

### Windows

Save the 32-bit and 64-bit `libdmtx.dll` files to `libdmtx-32.dll` and
`libdmtx-64.dll` respectively, in the root of this repo.
The `load_libdmtx` function in `wrapper.py` looks for the appropriate `DLL`
on `sys.path`. The appropriate `DLL` is packaged up into the wheel build,
then installed to the root of the virtual env. This strategy allows
the same method to be used when `pylibdmtx` is run from source, as an installed package and when included in a frozen binary.

## Releasing

1. Install tools.

```
pip install wheel
brew install pandoc
```

2. Build
    Generate the `reStructuredText README.rst` from `README.md` and create
    source and wheel builds. The `win32` and `win_amd64` will contain the
    appropriate `libdmtx.dll`.

    ```
    pandoc --from=markdown --to=rst README.md -o README.rst
    rm -rf build dist
    ./setup.py bdist_wheel
    ./setup.py bdist_wheel --plat-name=win32
    ./setup.py bdist_wheel --plat-name=win_amd64
    ```

3. Release to pypitest (see https://wiki.python.org/moin/TestPyPI for details)

    ```
    mkvirtualenv pypi
    pip install twine
    twine register -r pypitest dist/pylibdmtx-0.1.1-py2.py3-none-any.whl
    twine upload -r pypitest dist/*
    ```

4. Test the release to pypitest

    * Check https://testpypi.python.org/pypi/pylibdmtx/

    * If you are on Windows

    ```
    set PATH=%PATH%;c:\python35\;c:\python35\scripts
    \Python35\Scripts\mkvirtualenv.bat --python=c:\python27\python.exe test1
    ```

    * Install dependencies that are not on testpypi.python.org.
    If you are on Python 2.x, these are mandatory

    ```
    pip install enum34 pathlib
    ```

    * Pillow for tests and `read_datamatrix`. We can't use the
    `pip install pylibdmtx[scripts]` form here because `Pillow` will not be
    on testpypi.python.org

    ```
    pip install Pillow
    ```

    * Install the package itself

    ```
    pip install --index https://testpypi.python.org/simple pylibdmtx
    ```

    * Test

    ```
    read_datamatrix --help
    read_datamatrix <path-to-datamatrix.png>
    ```

5. If all is well, release to PyPI

    ```
    twine register dist/pylibdmtx-0.1.1-py2.py3-none-any.whl
    twine upload dist/*
    ```

    * Check https://pypi.python.org/pypi/pylibdmtx/

    * Install!

    ```
    pip install pylibdmtx[scripts]
    ```
