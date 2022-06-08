from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nkmodel",
    version="0.0.7",
    author="Edward L Platt",
    author_email="ed@elplatt.com",
    description="Implementation of Kauffman NK Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elplatt/nkmodel",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
