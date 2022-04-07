import setuptools
from setuptools import setup

setup(
    name="pypara",
    version="0.1",
    author="szsdk",
    install_requires=["click", "click_default_group", "more_itertools", "toolz"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'pypara = bin.pypara:cli',
        ],
    },
)
