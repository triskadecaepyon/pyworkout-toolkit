#! /usr/bin/env python
"""
A setuptools file for the pyworkout-toolkit
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyworkout-toolkit',

    version='0.0.1',

    description='Python tools to process workout data and telemetry',
    long_description=long_description,

    url='https://github.com/triskadecaepyon/pyworkout-toolkit/',

    maintainer='David Liu',
    maintainer_email='dcltechnology@gmail.com',

    license='BSD',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='workout data telemetry',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['numpy', 'pandas', 'lxml'],

)
