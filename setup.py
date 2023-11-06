from setuptools import setup

setup(
    name='strings_repository',
    version='0.1.0',
    description='Simple commandline tool for pulling data from strings repository (https://github.com/HereTrix/strings_repository)',
    url='https://github.com/HereTrix/strings_repository_cli',
    author='HereTrix',
    license='MIT',
    packages=['strings_repository'],
    install_requires=[
        'typer',
        'pyyaml',
        'requests',
    ],
    scripts=['bin/strings_repository'],
    zip_safe=False,
)
