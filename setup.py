import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools import find_packages

package_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(package_directory, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

with open(os.path.join(package_directory, "requirements.txt")) as req_file:
    requirements = req_file.readlines()

on_rtd = os.environ.get("READTHEDOCS") == "True"
if on_rtd:
    requirements = []

setup_args = dict(
    name="howmany",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    version="0.2.1",
    author="Andrew Tavis McAllister",
    author_email="andrew.t.mcallister@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    description="Wikidata powered comparisons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="new BSD",
    url="https://github.com/andrewtavis/howmany",
)

if __name__ == "__main__":
    setup(**setup_args)
