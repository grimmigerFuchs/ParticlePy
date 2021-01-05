# setup.py

import setuptools

setuptools.setup(
    name="pyticles",
    version="0.1.1",
    author="grimmigerFuchs",
    author_email="grimmigerfuchs@gmail.com",
    url="https://github.com/grimmigerfuchs/pyticles",
    license="MIT",
    description="A short library for easy to use particles in Pygame based on DaFluffyPotato's particle system.",
    packages=["pyticles"],
    install_requires=[
        "pygame~=2.0.1",
    ],
    python_requires='>=3.6'
)
