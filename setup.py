import os
import codecs

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as file:

    long_description = "\n" + file.read()

VERSION = '1.0.2'
DESCRIPTION = 'Face recognition via Search4Faces API'

setup(
    name="Search4Faces",
    version=VERSION,
    author="Nikita Minaev",
    author_email="<nikita@minaev.su>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['httpx', 'pydantic'],
    keywords=['python', 'face recognition', 'search4faces', 'ai'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    url='https://github.com/nikitalm8/Search4FacesAPI'
)