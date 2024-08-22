<h1 align="center">openassetpricing</h1>

<p align="center">
<b><i>Retrieve Open Source Asset Pricing Data (Chen and Zimmermann)</i></b>
</p>

**openassetpricing** is a Python package to download data from Open
Source Asset Pricing (OSAP).

There are 212 cross-sectional predictors.

- **Download predictor portfolio returns**: various portfolio construction
  methods: original paper methods, deciles, quintiles, equal-weighted,
  value-weighted, price filter, and so on ...
- **Download firm characteristics**: 209 from OSAP + 3 from CRSP (Price, Size, STreversal)

Learn more about Chen and Zimmermann data:
[Data website](https://www.openassetpricing.com/) |
[Github code](https://github.com/OpenSourceAP/CrossSection/) |
[Publication](https://www.nowpublishers.com/article/Details/CFR-0112)

## Installation
- **Option 1: install from PyPI**
```bash
pip install openassetpricing

# To upgrade
pip install -U openassetpricing
```

- **Option 2: local installation**
1. Download the package

If you have **git** installed, run in the terminal
```bash
git clone https://github.com/mk0417/open-asset-pricing-download
```

If you do not have **git**, you can download the pakage by clicking
the green `Code` button on top of the page and then clicking `Download ZIP`.

2. Install on your local machine

Run in the terminal
```bash
pip install <local path to the package>
```

Or, navigate to the package directory first, then run in the terminal
```bash
pip install .
```

## Usage
Both Pandas and Polars dataframes are supported. You can choose the
one that fits your workflow.

### Import package
```python
import openassetpricing as oap

openap = oap.OpenAP()
```

### List available datasets
You will see original dataset name of Chen and Zimmermann
```python
openap.list_datasets()
```

### Download list of predictors
```python
# Use Polars dataframe
df = openap.dl('signal_doc', 'polars')

# Use Pandas dataframe
df = openap.dl('signal_doc', 'pandas')
```

### Download portfolio returns
#### Download all predictors
```python
# Download OP portfolio returns in Polars dataframe
df = openap.dl('port_op', 'polars')

# Download equal-weighted decile portfolio returns in Pandas dataframe
df = openap.dl('port_deciles_ew', 'pandas')
```

#### Download specific predictors
```python
# Download BM portfolio returns based on NYSE stocks only in Polars dataframe
df = openap.dl('port_nyse', 'polars', ['BM'])
# Download BM and 12-month momentum value-weighted
# quintile portfolio returns in Polars dataframe
df = openap.dl('port_quintiles_vw', 'polars', ['BM', 'Mom12m'])

# Use Pandas dataframe
df = openap.dl('port_nyse', 'pandas', ['BM'])
df = openap.dl('port_quintiles_vw', 'pandas', ['BM', 'Mom12m'])
```

### Download firm characteristics
#### Download all firm characteristics
```python
# Use Polars dataframe
df = openap.dl('char_predictors', 'polars')

# Use Pandas dataframe
df = openap.dl('char_predictors', 'pandas')
```

#### Download specific firm characteristics
```python
# Use Polars dataframe
df = openap.dl('char_predictors', 'polars', ['BM'])
df = openap.dl('char_predictors', 'polars', ['BM', 'Mom12m'])

# Use Pandas dataframe
df = openap.dl('char_predictors', 'pandas', ['BM'])
df = openap.dl('char_predictors', 'pandas', ['BM', 'Mom12m'])
```

### Note
- You need valid WRDS account.
- The code has been tested with *Python 3.10.14*.

### Contacts
- Peng Li (pl750@bath.ac.uk)
- Andrew Chen (andrew.y.chen@frb.gov)
- Tom Zimmermann (tom.zimmermann@uni-koeln.de)
