"""
Inputs: None; this script relies on setuptools metadata defined inline.
Outputs: Distributes the openassetpricing package with optional extras for examples.
How to run: Execute `pip install .` for the core install. To include example dependencies, run
"pip install '.[examples]'" (quote the extras when using shells like zsh).
"""

from setuptools import setup, find_packages

setup(
    name='openassetpricing',
    version='0.0.2',
    author='Peng Li, Andrew Chen, Tom Zimmermann',
    author_email='pl750@bath.ac.uk, andrew.y.chen@frb.gov, tom.zimmermann@uni-koeln.de',
    license='GPLv2',
    packages=find_packages(),
    install_requires=[
        'polars',
        'pandas',
        'requests',
        'tabulate',
        'wrds',
        'pyarrow',
        'beautifulsoup4'
    ],
    extras_require={
        'examples': [
            'matplotlib',
            'numpy',
            'scikit-learn',
            'seaborn',
            'statsmodels'
        ]
    },
)
