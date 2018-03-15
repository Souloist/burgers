from __future__ import absolute_import

import os

from setuptools import find_packages, setup


README = open(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "README.rst",
)).read()


third_party_dependencies = [
    "flask",
    "requests",
    "sqlalchemy",
    "cerberus",
]

tests_require = (
    "nose",
)


setup(
    name="burgers",
    author="Richard Shen",
    author_email="richardzhaoshen@gmail.com",
    description="Rest API for burger service",
    long_description=README,
    packages=find_packages(exclude=["ez_setup"]),
    include_package_data=True,
    zip_safe=False,
    test_suite="nose.collector",
    install_requires=third_party_dependencies,
    tests_require=tests_require,
    classifiers=[
        "Framework :: Flask",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    entry_points="""
        [console_scripts]
        flask=flask.cli:main
    """,
)
