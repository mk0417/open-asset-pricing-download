"""Offline regression checks for the CRSP CIZ signal migration.

Run from the repository root: python3 -m unittest discover -s tests -p test_crsp_signals.py -v
Inputs: synthetic CIZ rows, including missing/zero values and bid/ask prices.
Outputs: unittest results; temporary SQLite/parquet fixtures are removed.
No WRDS credentials or network connections are used.
"""

import math
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import pandas as pd
import polars as pl
from polars.testing import assert_frame_equal

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from openassetpricing import OpenAP


SIGNALS = ['Price', 'Size', 'STreversal']


class CrspSignalsTest(unittest.TestCase):
    def setUp(self):
        # Legacy negative prices marked bid/ask averages. CIZ stores their
        # magnitude with a separate flag, which these absolute-price formulas
        # do not need. Shares are in thousands, market equity in millions.
        self.raw = pd.DataFrame({
            'permno': [10001, 10001, 10002, 10003, 10004, 10005, 10006],
            'mthcaldt': pd.to_datetime([
                '2024-01-31', '2024-02-29', '2024-03-28', '2024-04-30',
                '2024-05-31', '2024-06-28', '2025-01-31']),
            'mthprc': [10., 6.5, 0., None, 20., 30., 40.],
            'mthret': [.1, -.2, None, .05, 0., -1., .025],
            'shrout': [2000., 4000., 1000., 1000., 0., None, 5000.],
        })
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.execute("ATTACH DATABASE ':memory:' AS crsp")
        self.db.execute(
            'CREATE TABLE crsp.msf_v2 '
            '(permno INTEGER, mthcaldt TEXT, mthprc REAL, mthret REAL, shrout REAL)')
        rows = self.raw.copy()
        rows['mthcaldt'] = rows['mthcaldt'].dt.strftime('%Y-%m-%d')
        rows = rows.astype(object).where(rows.notna(), None)
        self.db.executemany(
            'INSERT INTO crsp.msf_v2 VALUES (?, ?, ?, ?, ?)',
            rows.itertuples(index=False, name=None))
        # Execute the production SELECT against the CIZ-only schema, so wrong
        # table names or aliases cannot be hidden by a mocked result frame.
        self.connection = Mock()
        self.connection.raw_sql.side_effect = lambda query, date_cols: pd.read_sql_query(
            query, self.db, parse_dates=date_cols)
        connection_patch = patch(
            'openassetpricing.openap_download.wrds.Connection',
            return_value=self.connection)
        self.factory = connection_patch.start()
        self.addCleanup(connection_patch.stop)
        self.openap = OpenAP.__new__(OpenAP)

    def expected_signed(self):
        # Independent scalar expectations, including the legacy edge cases.
        return pl.DataFrame({
            'permno': pl.Series(self.raw['permno'].tolist(), dtype=pl.Int32),
            'yyyymm': pl.Series(
                [202401, 202402, 202403, 202404, 202405, 202406, 202501],
                dtype=pl.Int32),
            'Price': [-math.log(10), -math.log(6.5), math.inf, None,
                      -math.log(20), -math.log(30), -math.log(40)],
            'Size': [-math.log(20), -math.log(26), None, None, None,
                     None, -math.log(200)],
            'STreversal': [-.1, .2, 0., -.05, 0., 1., -.025],
        })

    def test_ciz_query_preserves_formulas_dates_units_and_missingness(self):
        result = self.openap._dl_signal_crsp3()
        assert_frame_equal(result, self.expected_signed())
        self.factory.assert_called_once_with()

    def test_individual_signals_preserve_signing_and_backends(self):
        for backend in ['polars', 'pandas']:
            for signed in [False, True]:
                with self.subTest(backend=backend, signed=signed):
                    with tempfile.TemporaryDirectory() as tmp:
                        path = Path(tmp) / 'signals.parquet'
                        self.expected_signed().select('permno', 'yyyymm').write_parquet(path)
                        self.openap._get_url = Mock(return_value=str(path))
                        actual = self.openap.dl_signal(backend, SIGNALS, signed=signed)
                    expected = self.expected_signed()
                    if not signed:
                        expected = expected.with_columns(pl.col(SIGNALS) * -1)
                    if backend == 'pandas':
                        self.assertIsInstance(actual, pd.DataFrame)
                        pd.testing.assert_frame_equal(actual, expected.to_pandas())
                    else:
                        assert_frame_equal(actual, expected)


if __name__ == '__main__':
    unittest.main()
