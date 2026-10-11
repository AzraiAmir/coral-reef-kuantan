"""
Azr.AI — Coral Reef Monitoring Package
Setup script for pip install -e .
"""

from setuptools import setup, find_packages

setup(
    name="azr-ai-coral-reef",
    version="0.1.0",
    description="Azr.AI: An Integrated Deep Learning Framework for Coral Species Detection, Health Assessment, and Connectivity Modelling",
    author="Muhammad Azrai bin Amir",
    author_email="azrai.amir@live.iium.edu.my",
    packages=find_packages(include=["src", "src.*"]),
    python_requires=">=3.10",
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)