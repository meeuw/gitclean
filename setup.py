import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="vcscheck",
    version="0",
    author="Dick Marinus",
    author_email="dick@mrns.nl",
    description=
    ("Run code reformatting tools only for the changed lines in your version control system"
     ),
    license="GPL-3",
    keywords="vcs lint code formatting",
    url="http://packages.python.org/an_example_pypi_project",
    packages=['vcscheck', 'tests'],
    long_description=read('README.md'),
    entry_points={'console_scripts': ['git-check=vcscheck.vcscheck:gitcheck']},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPL-3 License",
    ],
    install_requires=[
        'click',
        'yapf',
    ], )
