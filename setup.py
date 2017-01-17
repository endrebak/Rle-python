
import sys
from setuptools import setup, find_packages

install_requires = ["numpy"]


setup(
    name="pyranges",
    packages=find_packages(),
    version="0.0.1",
    description="PhD",
    author=["Simon Meinhard"],
    author_email="simon.meinhard@epfl.ch",
    url="https://github.com/smeinhard/Rle-python",
    keywords=["Bioinformatics"],
    license=["MIT"],
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment", "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Scientific/Engineering"
    ],
    long_description=("See README.md"))

