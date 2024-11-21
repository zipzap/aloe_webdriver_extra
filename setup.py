"""
Setup script.
"""

from setuptools import setup, find_packages

if __name__ == '__main__':
    with \
            open('requirements.txt') as requirements:
        setup(
            packages=find_packages(),
            include_package_data=True,

            setup_requires=['setuptools_scm'],

            install_requires=requirements.readlines(),
        )
