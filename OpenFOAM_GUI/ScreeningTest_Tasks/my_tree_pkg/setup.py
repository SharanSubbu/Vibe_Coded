from setuptools import setup, find_packages

setup(
    name="tree_pkg",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'pyyaml',
    ],
)