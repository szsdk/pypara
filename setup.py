import setuptools
from setuptools import setup

setup(
    name="pypara",
    version="0.1",
    author="szsdk",
    scripts=["bin/pypara"],
    install_requires=["click", "more_itertools", "toolz"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
)
