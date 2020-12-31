#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


parsed_requirements = parse_requirements(
    'requirements/install.txt',
    session='workaround'
)

parsed_test_requirements = parse_requirements(
    'requirements/test.txt',
    session='workaround'
)

parsed_dev_requirements = parse_requirements(
    'requirements/develop.txt',
    session='workaround'
)


requirements = [str(ir.req) for ir in parsed_requirements]
test_requirements = [str(tr.req) for tr in parsed_test_requirements]
setup_requirements = [str(tr.req) for tr in parsed_dev_requirements]

setup(
    author="Surya Sankar",
    author_email='suryashankar.m@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="DiffBuddy provides helper methods to smass files and branches",
    entry_points={
        'console_scripts': [
            'diffbuddy=diffbuddy.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='diffbuddy',
    name='diffbuddy',
    packages=find_packages(include=['diffbuddy', 'diffbuddy.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/suryasankar/diffbuddy',
    version='0.1.0',
    zip_safe=False,
)
