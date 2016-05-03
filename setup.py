# coding=utf-8
from setuptools import setup
from setuptools import find_packages

setup(
    name="Steganography - NEL Phase Lab",
    version="0.0.1",
    author="Michał Krawczyk",
    author_email="krawczyk.michal91@gmail.com",
    packages=find_packages(),
    install_requires=["pika", "NetfilterQueue==0.6", "transitions"],
)
