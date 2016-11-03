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
PATH=/Users/lawh/local/python-2.7.12/bin:/Users/lawh/local/python-3.4.5/bin:/Users/lawh/local/python-3.5.2/bin:$PATH
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

Generate the `reStructuredText README`

```
pip install wheel
brew install pandoc
```

```
pandoc --from=markdown --to=rst README.md -o README.rst
rm -rf build dist
./setup.py sdist
./setup.py bdist_wheel
./setup.py bdist_wheel --plat-name=win32
./setup.py bdist_wheel --plat-name=win_amd64
```
