# setup.py

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyticles",
    version="0.1.0",
    author="grimmigerFuchs",
    author_email="grimmigerfuchs@gmail.com",
    url="https://github.com/grimmigerfuchs/pyticles",
    license="MIT",
    description="A short library for easy to use particles in Pygame based on DaFluffyPotato's particle system.",
    long_description=long_description,
    long_description_content_type="text/markup",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
