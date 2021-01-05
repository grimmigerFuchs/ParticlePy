#!/usr/bin/python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyticles-grimmigerFuchs",
    version="0.1.1",
    author="grimmigerFuchs",
    author_email="author@example.com",
    description="A short library for easy to use particles in Pygame based on DaFluffyPotato's particle system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grimmigerfuchs/pyticles",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)