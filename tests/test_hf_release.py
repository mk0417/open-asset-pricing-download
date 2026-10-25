# Smoke test: download from every Hugging Face release, without WRDS.
# How to run (from the repo root): python3 tests/test_hf_release.py
# Inputs: network access to huggingface.co
# Outputs: printed shapes and schemas; raises AssertionError on failure
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import openassetpricing as oap
from openassetpricing import urls
import polars as pl
from polars.testing import assert_series_equal


oap.list_release()

# ===== Every release: file map, one small portfolio and signal download =====
releases = sorted(
    int(i[len('release'):-len('_hf')]) for i in dir(urls)
    if i.startswith('release') and i.endswith('_hf'))
for release in releases:
    openap = oap.OpenAP(release)
    names = set(openap.name_id_map['download_name'])
    assert {'op', 'firm_char', 'firm_char_unsigned'} <= names, release
    df = openap.dl_port('op', 'polars', ['BM'])
    assert set(df['signalname'].unique()) == {'BM'}, release
    assert df.schema['port'] == pl.String and df.schema['date'] == pl.Date
    s = openap.dl_signal('polars', ['BM'])
    assert s.columns == ['permno', 'yyyymm', 'BM'] and len(s) > 0, release
    print(release, openap.hf_revision, len(names), 'datasets', df.shape, s.shape)

# Older release names still work
assert oap.OpenAP(2023).hf_revision == '2023.08'
assert oap.OpenAP(2022).hf_revision == '2022.03'

# Missing datasets and releases raise clear errors
openap = oap.OpenAP(202204)
for call in [lambda: openap.dl_port('daily_op_ew', 'polars', ['BM']),
             lambda: oap.OpenAP(201901),
             lambda: oap.OpenAP(hf_revision='2020.05')]:
    try:
        call()
    except ValueError as e:
        print('ValueError:', e)
    else:
        raise AssertionError('expected ValueError')

# Releases before 2022.03 have no SignalDoc
assert oap.OpenAP(202104).signal_sign is None

# ===== Default release, full checks =====
openap = oap.OpenAP()
assert openap.hf_revision == 'Data-Release-2026.10'
openap.list_port()

doc = openap.dl_signal_doc('polars')
assert {'Acronym', 'Sign'} <= set(doc.columns)
print(doc.shape)

for name in ['op', 'deciles_vw', 'holdper12', 'daily_op_ew']:
    df = openap.dl_port(name, 'polars', ['BM', 'Mom12m'])
    assert set(df['signalname'].unique()) == {'BM', 'Mom12m'}
    assert df.schema['port'] == pl.String and df.schema['date'] == pl.Date
    print(name, df.shape)

df = openap.dl_port('op', 'pandas', ['AM'])
print(type(df), df.shape)

# Signed vs unsigned: BM has sign +1, so pick a signal with sign -1
neg = doc.filter(pl.col('Sign') == -1, pl.col('Cat.Signal') == 'Predictor')
neg = neg['Acronym'][0]
u = openap.dl_signal('polars', ['BM', neg])
s = openap.dl_signal('polars', ['BM', neg], signed=True)
a = openap.dl_all_signals('polars', ['BM', neg])
assert u.columns == ['permno', 'yyyymm', 'BM', neg]
# Some releases' signed and unsigned files were written separately and
# differ by float rounding (~1e-14), so compare with a tolerance
assert_series_equal(u['BM'], s['BM'], check_exact=False)
assert_series_equal(u[neg], -s[neg], check_exact=False, check_names=False)
assert s.equals(a)
print(neg, u.shape)

# hf_revision override points at a branch directly
assert oap.OpenAP(hf_revision='Test-Data-2026.10').source == 'hf'
print('All checks passed')
