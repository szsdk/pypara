from setuptools import setup

setup(
    name="pypara",
    version="0.1",
    author="szsdk",
    scripts=["pypara", "pyr"],
    install_requires=["click", "more_itertools", "toolz"],
)
