#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from glob import glob

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

scripts = glob('scripts/*.py')


setup(
    name='pseudomonas_maize_genome',
    version='0.1.0',
    description="Code associated with the pseudomonas_maize_genome project",
    long_description=readme + '\n\n' + history,
    author="Nick Youngblut",
    author_email='nyoungb2@gmail.com',
    url='https://github.com/nick-youngblut/pseudomonas_maize_genome',
    packages=[
        'pseudomonas_maize_genome',
    ],
    package_dir={'pseudomonas_maize_genome':
                 'pseudomonas_maize_genome'},
    entry_points={
        'console_scripts': [
            'pseudomonas_maize_genome=pseudomonas_maize_genome.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    scripts=scripts,
    license="MIT license",
    zip_safe=False,
    keywords='pseudomonas_maize_genome',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
