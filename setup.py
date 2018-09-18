#!/usr/bin/env python

from setuptools import setup, find_packages

tests_require = ["coverage", "flake8", "wheel"]

setup(
    name="gpom",
    version="3.0.1",
    url="https://github.com/altlinuxteam/gpom3",
    license="Apache Software License",
    author="Sergey Bubnov",
    author_email="omg@altlinux.com",
    description="Group Policy Object Manager",
    long_description=open("README.rst").read(),
    install_requires=[
        "setuptools",
        "xmltodict",
        "configparser",
        "python-ldap"
    ],
    tests_require=tests_require,
    extras_require={"test": tests_require},
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'gpom=gpom.cli.__main__:main'
        ],
    },
#    test_suite="test",
    classifiers=[
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Systems Administration"
    ]
)
