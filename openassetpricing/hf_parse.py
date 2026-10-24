# File map for releases hosted on Hugging Face
# The dataset repo is public, so files are read from their resolve URLs
# without login or token. Parquet files are read with polars, which only
# fetches the columns and row groups it needs.
# Releases do not all have the same files (e.g. no daily portfolios before
# 2021.04), so each release's map is built from its branch's file list.
from urllib.parse import quote
import polars as pl
import requests


# download_name: candidate paths in the dataset repo, first match is used.
# Later paths are older layouts (2021.03 used Full_Sets_Main/Extended).
HF_DATASETS = {
    'signal_doc': ['SignalDoc.csv'],
    'firm_char': ['Firm Level Characteristics/signed_predictors_dl_wide.parquet'],
    'firm_char_unsigned': ['Firm Level Characteristics/Predictors.parquet'],
    # Monthly portfolios
    'op': [
        'Portfolios/Full Sets OP/PredictorPortsFull.parquet',
        'Portfolios/Full_Sets_Main/PredictorPortsFull.parquet'],
    'placebo_op': [
        'Portfolios/Full Sets OP/PlaceboPortsFull.parquet',
        'Portfolios/Full_Sets_Extended/PlaceboPortsFull.parquet'],
    'deciles_ew': ['Portfolios/Full Sets Alt/PredictorAltPorts_Deciles.parquet'],
    'deciles_vw': ['Portfolios/Full Sets Alt/PredictorAltPorts_DecilesVW.parquet'],
    'ex_nyse_p20_me': [
        'Portfolios/Full Sets Alt/'
        'PredictorAltPorts_LiqScreen_ME_gt_NYSE20pct.parquet'],
    'nyse': ['Portfolios/Full Sets Alt/PredictorAltPorts_LiqScreen_NYSEonly.parquet'],
    'ex_price5': [
        'Portfolios/Full Sets Alt/PredictorAltPorts_LiqScreen_Price_gt_5.parquet'],
    'vw_force': [
        'Portfolios/Full Sets Alt/PredictorAltPorts_LiqScreen_VWforce.parquet'],
    'quintiles_ew': ['Portfolios/Full Sets Alt/PredictorAltPorts_Quintiles.parquet'],
    'quintiles_vw': ['Portfolios/Full Sets Alt/PredictorAltPorts_QuintilesVW.parquet'],
    'ff93': ['Portfolios/Full Sets Alt/PredictorAltPorts_FF93style.parquet'],
    'holdper1': ['Portfolios/Full Sets Alt/PredictorAltPorts_HoldPer_1.parquet'],
    'holdper3': ['Portfolios/Full Sets Alt/PredictorAltPorts_HoldPer_3.parquet'],
    'holdper6': ['Portfolios/Full Sets Alt/PredictorAltPorts_HoldPer_6.parquet'],
    'holdper12': ['Portfolios/Full Sets Alt/PredictorAltPorts_HoldPer_12.parquet'],
    # Daily portfolios
    'daily_op_ew': ['DailyPortfolios/Predictor.parquet'],
    'daily_op_vw': ['DailyPortfolios/PredictorVW.parquet'],
    'daily_deciles_ew': ['DailyPortfolios/CtsPredictorDecile.parquet'],
    'daily_deciles_vw': ['DailyPortfolios/CtsPredictorDecileVW.parquet'],
    'daily_quintiles_ew': ['DailyPortfolios/CtsPredictorQuintile.parquet'],
    'daily_quintiles_vw': ['DailyPortfolios/CtsPredictorQuintileVW.parquet'],
}


def _get_hf_url(url_prefix, revision, path):
    return f'{url_prefix}/{quote(revision, safe="")}/{quote(path)}'


def _get_hf_files(api_prefix, revision):
    # All file paths on the branch. The tree API pages its results and gives
    # the next page in the Link header
    url = f'{api_prefix}/tree/{quote(revision, safe="")}?recursive=true'
    files = []
    while url:
        res = requests.get(url, timeout=60)
        if res.status_code == 404:
            raise ValueError(
                f'Hugging Face branch {revision!r} not found. '
                'Run list_release() to see available releases.')
        res.raise_for_status()
        files += [i['path'] for i in res.json() if i['type'] == 'file']
        url = res.links.get('next', {}).get('url')
    return set(files)


def _get_hf_name_id_map(url_prefix, api_prefix, revision):
    # Columns: name, full_name, file_id, download_name
    files = _get_hf_files(api_prefix, revision)
    rows = []
    for download_name, paths in HF_DATASETS.items():
        path = next((i for i in paths if i in files), None)
        if path:
            rows.append({
                'name': path.split('/')[-1],
                'full_name': path,
                'file_id': _get_hf_url(url_prefix, revision, path),
                'download_name': download_name})

    if not any(i['download_name'] == 'op' for i in rows):
        raise ValueError(
            f'Hugging Face branch {revision!r} does not have the file layout '
            'this package reads (releases before 2021.03 are not supported).')
    return pl.DataFrame(rows)
