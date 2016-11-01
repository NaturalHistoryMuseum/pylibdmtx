#!/usr/bin/env python
import io
import os
import sys

import pylibdmtx


SCRIPTS = ['read_datamatrix']

# Optional dependency
PILLOW = 'Pillow>=3.2.0'

setup_data = {
    'name': 'pylibdmtx',
    'version': pylibdmtx.__version__,
    'author': 'Lawrence Hudson',
    'author_email': 'l.hudson@nhm.ac.uk',
    'url': 'https://github.com/NaturalHistoryMuseum/pylibdmtx/',
    'license': 'LICENSE.txt',
    'description': pylibdmtx.__doc__,
    'long_description':
        ('View the github page (https://github.com/NaturalHistoryMuseum/pylibdmtx) '
         'for more details.'),
    'packages': ['pylibdmtx', 'pylibdmtx.tests'],
    'include_package_data': True,
    'test_suite': 'pylibdmtx.tests',
    'scripts': ['pylibdmtx/scripts/{0}.py'.format(script) for script in SCRIPTS],
    'entry_points': {
        'console_scripts':
            ['{0}=pylibdmtx.scripts.{0}:main'.format(script) for script in SCRIPTS],
    },
    'extras_require': {
        'scripts': [PILLOW],
    },
    'tests_require': [
        'nose>=1.3.4',
        PILLOW
    ],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
}


if 2 == sys.version_info[0]:
    # Extra dependencies for Python 2.x
    # enum34
    install_requires = setup_data.get('install_requires', [])
    install_requires.append('enum34>=1.1.6')
    setup_data['install_requires'] = install_requires

    # pathlib required for testing
    tests_require = setup_data.get('tests_require', [])
    tests_require.append('pathlib>=1.0.1')
    setup_data['tests_require'] = tests_require


def setuptools_setup():
    from setuptools import setup
    setup(**setup_data)


if (2, 7) == sys.version_info[:2] or (3, 4) <= sys.version_info:
    setuptools_setup()
else:
    sys.exit('Python versions 2.7 and >= 3.4 are supported')
