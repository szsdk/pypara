from setuptools import setup

setup(
    name             = 'pypara',
    version          = '0.1',
    author           = 'szsdk',
    # packages = ['pypara'],
    scripts=['pypara'],

    install_requires = [
        'termcolor', 'pyzmq'
    ],
)
