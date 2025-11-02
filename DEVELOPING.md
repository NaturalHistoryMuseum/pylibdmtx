## Development

```
python -m venv venv
source ./venv/bin/activate
pip install -U pip
pip install -r requirements.txt

python -m pytest --verbose --cov=pylibdmtx --cov-report=term-missing --cov-report=html pylibdmtx
python -m pylibdmtx.scripts.read_datamatrix pylibdmtx/tests/datamatrix.png
```

### Test matrix of supported Python versions

Run tox

```
rm -rf .tox && tox
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

1. Build

    Create source and wheel builds using the `build` package.

    ```
    rm -rf build dist pylibdmtx.egg-info
    python -m build
    ```

2. Release to pypitest (see https://packaging.python.org/guides/using-testpypi/)

    ```
    twine upload -r testpypi dist/*
    ```

3. Test the release to pypitest

    * Check https://test.pypi.org/project/pylibdmtx/

    * Create a test virtual environment

    ```
    python -m venv test_env
    source test_env/bin/activate  # On Windows: test_env\Scripts\activate
    ```

    * Install Pillow for tests and `read_datamatrix`. We can't use the
    `pip install pylibdmtx[scripts]` form here because `Pillow` will not be
    on testpypi.python.org

    ```
    pip install Pillow
    ```

    * Install the package itself

    ```
    pip install --index-url https://test.pypi.org/simple/ pylibdmtx
    ```

    * Test

    ```
    read_datamatrix --help
    read_datamatrix <path-to-datamatrix.png>
    ```

4. If all is well, release to PyPI

    ```
    twine upload dist/*
    ```

    * Check https://pypi.org/project/pylibdmtx/

    * Install!

    ```
    pip install pylibdmtx[scripts]
    ```
