#!/usr/bin/env python

import setuptools
import os

setuptools.setup(
    name='libgeosuiteprv',
    version='0.0.6',
    description='Parser for the GeoSuite<tm> PRV export format',
    long_description="""Parser for the GeoSuite<tm> PRV export format""",
    long_description_content_type="text/markdown",
    author='Egil Moeller, Craig William Christensen and others ',
    author_email='em@emeraldgeo.no, cch@emeraldgeo.no',
    url='https://github.com/emerald-geomodelling/libgeosuiteprv',
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "python-dateutil",
    ],
    entry_points = {
        'libsgfdata.parsers': ['prv=libgeosuiteprv:parse'],
    }
)
