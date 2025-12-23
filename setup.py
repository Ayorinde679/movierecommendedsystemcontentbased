from setuptools import setup, find_packages
import os
from pathlib import Path

here = Path(__file__).parent.resolve()
with open(here / 'README.md', encoding='utf-8') as f:
    long_description = f.read()
with open(here / 'requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()
setup(
    name='src',
    version="0.0.1",
    author='Ayorinde Ayokunle',
    description='A prototype for movie recomendation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package = "src",
    python_requires='>=3.7',
    install_requires=requirements,
    packages=find_packages(),
)










