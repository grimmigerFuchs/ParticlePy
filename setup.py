#!/usr/bin/python3
# setup.py

import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

if __name__ == "__main__":
    setuptools.setup(
        name="particlepy",
        version="1.0.2",
        license="MIT",
        author="grimmigerFuchs",
        author_email="grimmigerfuchs@gmail.com",
        description="A short library for easy to use particles in Pygame.",
        long_description=README,
        long_description_content_type="text/markdown",
        url="https://github.com/grimmigerFuchs/ParticlePy",
        packages=setuptools.find_packages(),
        install_requires=[
            "pygame"
        ],
        classifiers=[
            # https://pypi.python.org/pypi?%3Aaction=list_classifiers
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Topic :: Software Development"
        ],
        project_urls={
            "GitHub: repo": "https://github.com/grimmigerFuchs/ParticlePy",
            "Bugtracker": "https://github.com/grimmigerFuchs/ParticlePy/issues",
        },
        keywords=["pygame", "particle", "game", "simulation", "realtime", "rendering"],
        python_requires=">=3.6"
    )
