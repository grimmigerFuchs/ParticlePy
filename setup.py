#!/usr/bin/python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="particlepy",
    version="1.0.1",
    license="MIT",
    author="grimmigerFuchs",
    author_email="grimmigerfuchs@gmail.com",
    description="A short library for easy to use particles in Pygame based on DaFluffyPotato's particle system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grimmigerfuchs/particlepy",
    packages=setuptools.find_packages(),
    install_requires=[
        "pygame~=2.0.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="pygame particle torch dust easy game",
    python_requires='>=3.6',
    zip_safe=False
)
