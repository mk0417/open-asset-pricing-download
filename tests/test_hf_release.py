# Smoke test: download from the Hugging Face release and the latest Google
# Drive release, without WRDS.
# How to run (from the repo root): python3 tests/test_hf_release.py
# Inputs: network access to huggingface.co and drive.google.com
# Outputs: printed shapes and schemas; raises AssertionError on failure
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import openassetpricing as oap
import polars as pl


oap.list_release()

# ===== Hugging Face =====
openap = oap.OpenAP(202610)
assert openap.source == 'hf'
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
assert u['BM'].equals(s['BM']) and u[neg].equals(-s[neg])
assert s.equals(a)
print(neg, u.shape)

# hf_revision override points at a branch directly
assert oap.OpenAP(hf_revision='Test-Data-2026.10').source == 'hf'

# ===== Google Drive (backward compatibility) =====
openap = oap.OpenAP()
assert openap.source == 'gdrive'
df = openap.dl_port('op', 'polars', ['BM'])
print('gdrive op', df.shape)
df = openap.dl_signal('polars', ['BM'])
print('gdrive BM', df.shape)
print('All checks passed')
