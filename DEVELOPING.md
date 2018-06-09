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
PATH=~/local/python-2.7.14/bin:~/local/python-3.4.8/bin:~/local/python-3.5.5/bin:~/local/python-3.6.5/bin:$PATH
tox
```

### Windows

Save the 32-bit and 64-bit `libdmtx.dll` files to `libdmtx-32.dll` and
`libdmtx-64.dll` respectively, in the `pylibdmtx` directory.
The `load_pylibdmtx` function in `wrapper.py` looks for the appropriate `DLL`s.
The appropriate `DLL` is packaged up into the wheel build and is installed
alongside the package source. This strategy allows the same method to be used
when `pylibdmtx` is run from source, as an installed package and when included
in a frozen binary.

## Releasing

1. Install tools.

```
pip install wheel
```

2. Build
    Create source and wheel builds. The `win32` and `win_amd64` wheels will
    contain the appropriate `libdmtx.dll`.

    ```
    rm -rf build dist MANIFEST.in pylibdmtx.egg-info
    cp MANIFEST.in.all MANIFEST.in
    ./setup.py bdist_wheel

    cat MANIFEST.in.all MANIFEST.in.win32 > MANIFEST.in
    ./setup.py bdist_wheel --plat-name=win32

    # Remove these dirs to prevent win32 DLL from being included in win64 build
    rm -rf build pylibdmtx.egg-info
    cat MANIFEST.in.all MANIFEST.in.win64 > MANIFEST.in
    ./setup.py bdist_wheel --plat-name=win_amd64

    rm -rf build MANIFEST.in pylibdmtx.egg-info
    ```

3. Release to pypitest (see https://packaging.python.org/guides/using-testpypi/)

    ```
    mkvirtualenv pypi
    pip install twine
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
    twine upload dist/*
    ```

    * Check https://pypi.python.org/pypi/pylibdmtx/

    * Install!

    ```
    pip install pylibdmtx[scripts]
    ```
