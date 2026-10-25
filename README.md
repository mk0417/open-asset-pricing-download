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
git clone https://github.com/mk0417/open-asset-pricing-download.git
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

- **Optional example dependencies**

If you plan to run the example scripts and notebooks, install with extras:
```bash
pip install '.[examples]'
```

## Usage
Both Pandas and Polars dataframes are supported. You can choose the
one that fits your workflow.

### Import package
```python
import openassetpricing as oap

# List available release versions
oap.list_release()

# By default, it initializes the data source of most recent release
openap = oap.OpenAP()

# Specify the release version if you need vintage data, for example, 202408
openap = oap.OpenAP(202408)
```

### Data source: Hugging Face
All releases download from Hugging Face
([OpenSourceAP/CrossSection](https://huggingface.co/datasets/OpenSourceAP/CrossSection)),
one dataset branch per release: 2021.03 through 2026.10 (the default).
Earlier versions of this package downloaded from Google Drive.
```python
# Releases are named yyyymm; the older names 2023 and 2022 still work
openap = oap.OpenAP(202308)

# Or point at any branch of the dataset repo directly
openap = oap.OpenAP(hf_revision='Data-Release-2026.10')
```
Besides the portfolio sets above, releases include holding-period,
FF93-style, VW-forced, placebo, and daily portfolios. Older releases have
fewer files (no daily portfolios before 2021.04 or in 2022.04; 2021.03 has
only `op`, `placebo_op`, and firm characteristics), so run
`openap.list_port()` to see what a release has. Only the requested columns
and predictors are downloaded, so `dl_signal` and
`dl_port(..., predictor=[...])` are fast. The 2020.05 and 2020.07 releases
are on Hugging Face in an older format that this package does not read.

### List available portfolios (various implementations)
You will see original portfolio names of Chen and Zimmermann and the corresponding download names.
```python
openap.list_port()
```

### Download list of predictors
```python
# Use Polars dataframe
df = openap.dl_signal_doc('polars')

# Use Pandas dataframe
df = openap.dl_signal_doc('pandas')
```

### Download portfolio returns
#### Download all predictors
```python
# Download OP portfolio returns in Polars dataframe
df = openap.dl_port('op', 'polars')

# Download equal-weighted decile portfolio returns in Pandas dataframe
df = openap.dl_port('deciles_ew', 'pandas')
```

#### Download specific predictors
```python
# Download BM portfolio returns based on NYSE stocks only in Polars dataframe
df = openap.dl_port('nyse', 'polars', ['BM'])
# Download BM and 12-month momentum value-weighted
# quintile portfolio returns in Polars dataframe
df = openap.dl_port('quintiles_vw', 'polars', ['BM', 'Mom12m'])

# Use Pandas dataframe
df = openap.dl_port('nyse', 'pandas', ['BM'])
df = openap.dl_port('quintiles_vw', 'pandas', ['BM', 'Mom12m'])
```

### Download firm characteristics
#### Download all firm characteristics
```python
# Use Polars dataframe
df = openap.dl_all_signals('polars')

# Use Pandas dataframe
df = openap.dl_all_signals('pandas')
```

#### Download specific firm characteristics
```python
# Use Polars dataframe
df = openap.dl_signal('polars', ['BM'])

# Use Pandas dataframe
df = openap.dl_signal('pandas', ['BM'])
```

### Note
- To download all signals, you need a WRDS account.
- `Price`, `Size`, and `STreversal` are computed from WRDS `crsp.msf_v2`
  (CRSP CIZ). The signed formulas remain `-log(abs(price))`,
  `-log(abs(price) * shrout / 1000)`, and `-return`, respectively; missing
  returns remain zero and nonfinite size remains missing. `dl_signal` defaults
  to unsigned values; `dl_all_signals` returns signed values. CIZ monthly
  returns use different dividend reinvestment and delisting conventions, so
  historical `STreversal` values can differ from the legacy `crsp.msf` data.
  Revised prices, shares, and coverage can also change `Price` and `Size`.
  See the [WRDS transition guide](https://wrds-www.wharton.upenn.edu/documents/2084/Webinar.pdf).
  These three signals use the WRDS data available when called, independently
  of the selected OpenAP release vintage.
- The code has been tested with *Python 3.10.14*.

Offline CRSP regression checks can be run with
`python3 -m unittest discover -s tests -p test_crsp_signals.py -v`.

### Contacts
- Peng Li (pl750@bath.ac.uk)
- Andrew Chen (andrew.y.chen@frb.gov)
- Tom Zimmermann (tom.zimmermann@uni-koeln.de)
