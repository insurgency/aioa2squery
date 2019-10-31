#! /usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='aioa2squery',
    version='0.0.1',
    author='insurgency.gg',
    url='https://github.com/insurgency/aioa2squery',
    packages=find_packages(
        exclude=[
            'tests',
        ],
    ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: First Person Shooters',
        'Topic :: Internet',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
    license='MIT',
    python_requires='>=3.8',
    test_suite='tests',
    extras_require={
        'speedups': [
            'uvloop==0.14.0rc2',
        ],
    },
    # Automatic Script Creation
    # https://setuptools.readthedocs.io/en/latest/setuptools.html#automatic-script-creation
    entry_points={
        'console_scripts': [
            'a2squery = aioa2squery.command:main'
        ],
    },
)
