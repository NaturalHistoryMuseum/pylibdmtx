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

If you use non-standard locations, tell where your python builds are before
running `tox` for the first time.

```
PATH=/Users/lawh/local/python-2.7.12/bin:/Users/lawh/local/python-3.4.5/bin:/Users/lawh/local/python-3.5.2/bin:$PATH

tox
```

## Releasing

Generate the `reStructuredText README`

```
pandoc --from=markdown --to=rst README.md -o README.rst
```
