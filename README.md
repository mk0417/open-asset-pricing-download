<p align="center">
<b>openassetpricing</b><br>
<i>retrieve Open Source Asset Pricing Data (Chen and
Zimmermann)</i>
</p>

**openassetpricing** is a Python package to download predictor portfolio
returns and firm characteristics data from Chen and Zimmermann project
of **Open Source Asset Pricing**.

If you need more details about the data, please go to
- [Data website](https://www.openassetpricing.com/)
- [Github code](https://github.com/OpenSourceAP/CrossSection/)
- [Publication](https://www.nowpublishers.com/article/Details/CFR-0112)

## Installation
- Option 1: install from PyPI
```bash
pip install openassetpricing
```

- Option 2: local installation
1. Download the package

If you have **git** installed, run in the terminal
```bash
git clone
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

### Import pacakge
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
df = openap.dl('', 'pandas')
```

#### Download specific predictors
```python
# Download BM portfolio returns based on NYSE stocks only in Polars dataframe
df = openap.dl('port_nyse', 'polars', ['BM'])
# Download BM and 12-month momentum value-weighted quintile portfolio returns in Polars dataframe
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
The code has been tested with *Python 3.10.14*.
