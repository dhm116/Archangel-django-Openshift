#!/usr/bin/env python

from setuptools import setup

setup(
    name='YourAppName',
    version='1.0',
    description='OpenShift App',
    author='Your Name',
    author_email='example@example.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Django>=1.3','psycopg2', 'django_evolution', 'model_utils', 'rest_framework'],
)
