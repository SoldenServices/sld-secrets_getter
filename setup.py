#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ["boto3", "botocore", ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Matthew Larsen",
    author_email='matt.larsen@connorgp.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Thin wrapper for the AWS Secrets Manager library. Allows for getting secrets in a standard way.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='Secrets Manager',
    name='sld.secrets_getter',
    packages=find_packages(include=['secrets_getter', 'secrets_getter.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SoldenServices/sld.secrets_getter',
    version='0.2.5',
    zip_safe=False,
)
