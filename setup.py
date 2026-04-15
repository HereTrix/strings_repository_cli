from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='strings_repository',
    version='1.0.0',
    description='Simple commandline tool for pulling data from strings repository (https://github.com/HereTrix/strings_repository)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HereTrix/strings_repository_cli',
    download_url='https://github.com/HereTrix/strings_repository_cli/archive/refs/tags/1.0.0.tar.gz',
    author='HereTrix',
    license='MIT',
    packages=['strings_repository'],
    install_requires=[
        'typer',
        'pyyaml',
        'requests',
    ],
    scripts=['bin/strings_repository'],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',
    ]
)
