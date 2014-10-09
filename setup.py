#!/usr/bin/env python
"""
sentry-sqwiggle
===============

An extension for Sentry to integrate with Sqwiggle that sends notifications
to a sqwiggle stream when new errors are reported.

:copyright: (c) 2011 by the Linovia, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""


from setuptools import setup, find_packages


install_requires = [
    'sentry>=4.6.0',
]

test_requires = [
]


setup(
    name='sentry-sqwiggle',
    version='0.1.0',
    author='Emil Ahlbäck',
    author_email='e.ahlback@gmail.com',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require={'test': test_requires},
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'sentry_sqwiggle = sentry_sqwiggle '
        ],

       'sentry.plugins': [
            'sqwiggle = sentry_sqwiggle.models:SqwiggleMessage'
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)