"""Download published OpenAP data and compute three CRSP characteristics.

Usage: import OpenAP from openassetpricing and call its dl_* methods.
Inputs: release files on Hugging Face and, for Price/Size/STreversal, WRDS CRSP CIZ.
Outputs: pandas or Polars dataframes.
"""

from . import urls
from .hf_parse import _get_hf_name_id_map
import polars as pl
from tabulate import tabulate
import wrds
import re
import time


def list_release():
    df = (
        pl.DataFrame(
            [(int(re.findall(r'^release(\d+)_hf$', i)[0]), getattr(urls, i))
             for i in dir(urls) if re.match(r'^release\d+_hf$', i)],
            schema=['release', 'branch'], orient='row')
        .with_columns(
            default=pl.when(pl.col('release')==urls.default_release)
            .then(pl.lit('*')).otherwise(pl.lit('')))
        .sort('release')
    )
    table = [i for i in df.iter_rows()]
    headers = ['Release', 'Hugging Face branch', 'Default']
    print(tabulate(table, headers, tablefmt='simple_outline'))

class OpenAP:
    def __init__(self, release_year=None, hf_revision=None):
        # hf_revision overrides the Hugging Face branch set in urls.py,
        # e.g. to try a new release before the package is updated
        if not release_year:
            release_year = urls.default_release
        release_year = urls.release_aliases.get(int(release_year), release_year)
        self.release_year = release_year
        self.hf_revision = (
            hf_revision or getattr(urls, f'release{release_year}_hf', None))
        if not self.hf_revision:
            raise ValueError(
                f'Release {release_year} is not available. '
                'Run list_release() to see available releases.')
        self.source = 'hf'

        self.name_id_map = _get_hf_name_id_map(
            urls.hf_url_prefix, urls.hf_api_prefix, self.hf_revision)

        # Releases before 2022.03 have no SignalDoc.csv
        self.signal_sign = None
        if 'signal_doc' in self.name_id_map['download_name']:
            self.signal_sign = (
                pl.read_csv(
                    self._get_url('signal_doc'), infer_schema_length=300,
                    columns=['Acronym', 'Sign'], null_values='NA')
                .rename({'Acronym': 'signal', 'Sign': 'sign'})
                .with_columns(pl.col('sign').cast(pl.Int8))
            )

    def list_port(self):
        df = (
            self.name_id_map
            .filter(pl.col('full_name').str.contains('Portfolios/'))
            .select('name', 'download_name')
        )
        table = [i for i in df.iter_rows()]
        headers = ['CZ portfolio file', 'Name for download']
        print(tabulate(table, headers, tablefmt='simple_outline'))

    def _get_url(self, data_name):
        data_header = self.name_id_map.filter(pl.col('download_name')==data_name)
        if data_header.is_empty():
            raise ValueError(
                f'Dataset {data_name!r} is not available in release '
                f'{self.hf_revision}. Run list_port() to see available '
                'portfolios.')
        self.url = data_header[0, 'file_id']
        return self.url

    def _convert_to_backend(self, df, df_backend):
        if df_backend == 'polars':
            return df
        if df_backend == 'pandas':
            return df.to_pandas()

    def _dl_signal_crsp3(self):
        conn = wrds.Connection()

        # CIZ replaces the legacy monthly file (last updated through 2024).
        # Alias its fields so the signal formulas below remain unchanged.
        # shrout is still in thousands; mthret uses native CIZ compounding
        # and delisting treatment, so historical STreversal can differ.
        df = conn.raw_sql(
            """
            select permno, mthcaldt as date, mthprc as prc,
                   mthret as ret, shrout
            from crsp.msf_v2
            """, date_cols=['date']
        )

        # They are signed
        df = (
            pl.from_pandas(df)
            .select(
                pl.col('permno').cast(pl.Int32),
                pl.col('date').dt.year().mul(100)
                .add(pl.col('date').dt.month())
                .cast(pl.Int32).alias('yyyymm'),
                pl.col('prc').abs().log().mul(-1).alias('Price'),
                pl.col('prc').abs().mul(pl.col('shrout')).truediv(1000)
                .log().mul(-1).alias('Size'),
                pl.col('ret').fill_null(0).mul(-1).alias('STreversal')
            )
            .with_columns(
                pl.when(pl.col('Size').is_finite())
                .then(pl.col('Size'))
                .alias('Size')
            )
        )
        return df

    def _dl_port_hf(self, df_backend, predictor=None):
        # Parquet is filtered before download, so only the requested
        # predictors are fetched
        lf = pl.scan_parquet(self.url)
        if predictor:
            if type(predictor) is not list:
                raise ValueError('Predictor must be a list')
            lf = lf.filter(pl.col('signalname').is_in(predictor))

        df = lf.collect()
        if predictor and df['signalname'].n_unique() != len(predictor):
            print('One or more input predictors are not available.')

        df = df.sort('signalname', 'port', 'date')
        return self._convert_to_backend(df, df_backend)

    def _dl_signal_hf(self, df_backend, predictor=None, signed=True,
                      crsp3_join='left'):
        # self.url is a wide parquet file: permno, yyyymm, one column per
        # signal. Price, Size and STreversal are not in the file and come
        # from CRSP (signed by default)
        crsp3 = ['Price', 'Size', 'STreversal']
        lf = pl.scan_parquet(self.url)

        if not predictor:
            df = lf.collect().join(
                self._dl_signal_crsp3(), how='left', on=['permno', 'yyyymm'])
            df = df.sort('permno', 'yyyymm')
            return self._convert_to_backend(df, df_backend)

        if type(predictor) is not list:
            raise ValueError('Predictor must be a list')

        available = set(lf.collect_schema().names()) | set(crsp3)
        missing = [i for i in predictor if i not in available]
        if missing:
            raise ValueError(f'Predictors not available: {missing}')

        ex_crsp3 = [i for i in predictor if i not in crsp3]
        df = None
        if ex_crsp3:
            df = (
                lf.select('permno', 'yyyymm', *ex_crsp3)
                .filter(pl.any_horizontal(pl.col(ex_crsp3).is_not_null()))
                .collect()
            )

        if set(crsp3) & set(predictor):
            temp = self._dl_signal_crsp3()
            if not signed:
                temp = temp.with_columns(pl.col(crsp3).mul(-1))
            if df is None:
                df = temp
            else:
                df = df.join(
                    temp, how=crsp3_join, on=['permno', 'yyyymm'],
                    coalesce=True)

        df = (
            df.select('permno', 'yyyymm', *predictor)
            .filter(pl.any_horizontal(pl.col(predictor).is_not_null()))
            .with_columns(pl.col(predictor).cast(pl.Float64))
            .sort('permno', 'yyyymm')
        )
        return self._convert_to_backend(df, df_backend)

    def _print_time(self, time_used):
        if time_used <= 60:
            print(f'\nData is downloaded: {time_used:.0f}s')
        else:
            print(f'\nData is downloaded: {time_used/60:.0f} mins')

    def dl_signal_doc(self, df_backend):
        url = self._get_url('signal_doc')
        df = pl.read_csv(url, infer_schema_length=300)
        return self._convert_to_backend(df, df_backend)

    def dl_port(self, data_name, df_backend, predictor=None):
        if df_backend in ['polars', 'pandas']:
            self.url = self._get_url(data_name)
            start_time = time.time()
            df = self._dl_port_hf(df_backend, predictor)
            end_time = time.time()
            time_used = end_time - start_time
            self._print_time(time_used)
            return df
        else:
            raise ValueError("Unsupported backend. Choose 'polars' or 'pandas'.")

    def dl_all_signals(self, df_backend, predictor=None):
        if df_backend in ['polars', 'pandas']:
            self.url = self._get_url('firm_char')
            start_time = time.time()
            df = self._dl_signal_hf(df_backend, predictor)
            end_time = time.time()
            time_used = end_time - start_time
            self._print_time(time_used)
            return df
        else:
            raise ValueError("Unsupported backend. Choose 'polars' or 'pandas'.")

    def dl_signal(self, df_backend, predictor, signed=False):
        if df_backend in ['polars', 'pandas']:
            start_time = time.time()
            # Unsigned and signed versions are separate wide files
            data_name = 'firm_char' if signed else 'firm_char_unsigned'
            self.url = self._get_url(data_name)
            df = self._dl_signal_hf(
                df_backend, predictor, signed, crsp3_join='full')
            end_time = time.time()
            time_used = end_time - start_time
            self._print_time(time_used)
            return df
        else:
            raise ValueError("Unsupported backend. Choose 'polars' or 'pandas'.")
