#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md', encoding='utf-8') as history_file:
    history = history_file.read()

install_requires = [
    'mlblocks>=0.6.2',
    'pandas>=1.5.3',
    'numpy>=1.26.0',
    'scipy>=1.11.3',
]

setup_requires = [
    'pytest-runner>=2.11.1',
]

tests_require = [
    'pytest>=7.2.2',
    'pytest-cov>=4.1.0',
    'jupyter>=1.0.0,<2',
    'rundoc>=0.4.3,<0.5',
]

development_requires = [
    # general
    'bumpversion>=0.5.3,<0.6',
    'pip>=9.0.1',
    'watchdog>=0.8.3,<0.11',

    # docs
    'm2r>=0.2.0,<0.3',
    'Sphinx>=1.7.1,<3',
    'sphinx_rtd_theme>=0.2.4,<0.5',
    'autodocsumm>=0.1.10',
    'markupsafe<2.1.0',
    'Jinja2>=2,<3.1',

    # fails on Sphinx < v3.4
    'alabaster<=0.7.12',
    # fails on Sphins < v5.0
    'sphinxcontrib-applehelp<1.0.8',
    'sphinxcontrib-devhelp<1.0.6',
    'sphinxcontrib-htmlhelp<2.0.5',
    'sphinxcontrib-serializinghtml<1.1.10',
    'sphinxcontrib-qthelp<1.0.7',

    # style check
    'flake8>=3.7.7,<4',
    'flake8-absolute-import>=1.0,<2',
    'flake8-docstrings>=1.5.0,<2',
    'flake8-sfs>=0.0.3,<0.1',
    'isort>=4.3.4,<5',
    'pylint>=2.5.3,<3',

    # fix style issues
    'autoflake>=1.1,<2',
    'autopep8>=1.4.3,<2',

    # distribute on PyPI
    'twine>=1.10.0,<4',
    'wheel>=0.30.0',

    # Advanced testing
    'coverage>=4.5.1,<6',
    'tox>=2.9.1,<4',
    'importlib-metadata<5',
    'mistune<2',
    'invoke',
]

setup(
    author='MIT Data To AI Lab',
    author_email='dailabmit@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    description='Signal Processing Tools for Machine Learning',
    entry_points={
        'mlblocks': [
            'primitives=sigpro:MLBLOCKS_PRIMITIVES',
        ],
    },
    extras_require={
        'test': tests_require,
        'dev': development_requires + tests_require,
    },
    include_package_data=True,
    install_requires=install_requires,
    keywords='sigpro signal processing tools machine learning',
    license='MIT license',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    name='sigpro',
    packages=find_packages(include=['sigpro', 'sigpro.*']),
    python_requires='>=3.9,<3.13',
    setup_requires=setup_requires,
    test_suite='tests',
    tests_require=tests_require,
    url='https://github.com/sintel-dev/SigPro',
    version='0.3.1.dev0',
    zip_safe=False,
)
