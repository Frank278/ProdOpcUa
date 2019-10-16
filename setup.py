# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import opc


setup(
    name='opc',
    version=opc.__version__,
    description='',
    author='Pankraz Schmitt',
    author_email='pank24@gmx.net',
    include_package_data=True,
    url='https://github.com/Frank278/ProductionOpcUa/tree/ver-%s' % opc.__version__,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)

