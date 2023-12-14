#! /usr/bin/env python
import codecs
import sys
from setuptools import setup

__version__ = '1.3'


if sys.version_info >= (3, ):
    with codecs.open('README.rst', encoding='utf-8') as f:
        long_description = f.read()
else:
    with open('README.rst') as f:
        long_description = f.read()

setup(
    name="text-unidecode",
    version=__version__,
    description="The most basic Text::Unidecode port",
    long_description=long_description,
    license='Artistic License',
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    url='https://github.com/kmike/text-unidecode/',

    package_dir={'': 'src'},
    packages=['text_unidecode'],
    package_data={'text_unidecode': ['data.bin']},

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Artistic License',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
    ],
)
