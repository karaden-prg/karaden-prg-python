#!/usr/bin/env python

from setuptools import setup, find_packages
import karaden

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    "requests >= 2.28.2",
]

test_requirements = [
    "pytest"
    "pytest-mock"
    "httpretty"
]

setup(
    author=karaden.__author__,
    author_email=karaden.__email__,
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Japanese',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Telephony',
    ],
    description="Python library for the Karaden API",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords=['karaden', 'communication platform as a service', 'cpaas', 'sms', 'api'],
    name='karaden-prg-python',
    packages=find_packages(include=['karaden', 'karaden.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/karaden-prg/karaden-prg-python',
    version=karaden.__version__,
    zip_safe=False,
)
