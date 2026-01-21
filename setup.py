#!/usr/bin/env python

import os
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'karaden', '__version__.py'), encoding='utf-8') as fp:
    exec(fp.read(), about)

requirements = [
    "requests >= 2.28.2",
]

test_requirements = [
    "pytest"
    "pytest-mock"
    "httpretty"
]

setup(
    author=about['__author__'],
    author_email=about['__author_email__'],
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
    description=about['__description__'],
    install_requires=requirements,
    license=about['__license__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords=['karaden', 'communication platform as a service', 'cpaas', 'sms', 'api'],
    name=about['__title__'],
    packages=find_packages(include=['karaden', 'karaden.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url=about['__url__'],
    version=about['__version__'],
    zip_safe=False,
)
