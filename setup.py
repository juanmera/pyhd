#!/usr/bin/env python
# Copyright 2019 Juan Manuel Mera
# Distributed under the terms of GNU General Public License v3 (GPLv3)

from distutils.core import setup

setup(
    name='hd',
    version='0.1',
    description='HD keys using BIP21, BIP28 and BIP44',
    author='Juan Mera',
    author_email='juanmera@gmail.com',
    url='https://www.github.com/juanmera/pyhd',
    packages=['hd'],
    install_requires=['coincurve']
)