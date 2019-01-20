# -*- coding: utf-8 -*-

import os
from setuptools import setup
from tablelogger import __version__

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-table-logger',
    version=__version__,
    description=('A django package that allows easy'
                 ' logging of table changes to anywhere'),
    long_description=README,
    url='https://github.com/voltlines/django-table-logger',
    download_url='https://github.com/voltlines/django-table-logger/tarball/%s' % ( # noqa
        __version__,),
    author='Volt Lines',
    author_email='tech@voltlines.com',
    license='MIT',
    packages=['tablelogger'],
    include_package_data=True,
    install_requires=[
        'Django>=1.11'
    ]
)
