# File map for releases hosted on Hugging Face (2026.10 and later)
# The dataset repo is public, so files are read from their resolve URLs
# without login or token. Parquet files are read with polars, which only
# fetches the columns and row groups it needs.
from urllib.parse import quote
import polars as pl


# download_name: path in the dataset repo
HF_DATASETS = {
    'signal_doc': 'SignalDoc.csv',
    'firm_char': 'Firm Level Characteristics/signed_predictors_dl_wide.parquet',
    'firm_char_unsigned': 'Firm Level Characteristics/Predictors.parquet',
    # Monthly portfolios
    'op': 'Portfolios/Full Sets OP/PredictorPortsFull.parquet',
    'placebo_op': 'Portfolios/Full Sets OP/PlaceboPortsFull.parquet',
    'deciles_ew': 'Portfolios/Full Sets Alt/PredictorAltPorts_Deciles.parquet',
    'deciles_vw': 'Portfolios/Full Sets Alt/PredictorAltPorts_DecilesVW.parquet',
    'ex_nyse_p20_me': (
        'Portfolios/Full Sets Alt/'
        'PredictorAltPorts_LiqScreen_ME_gt_NYSE20pct.parquet'),
    'nyse': 'Portfolios/Full Sets Alt/PredictorAltPorts_LiqScreen_NYSEonly.parquet',
    'ex_price5': (
        'Portfolios/Full Sets Alt/PredictorAltPorts_LiqScreen_Price_gt_5.parquet'),
    'vw_force': (
        'Portfolios/Full Sets Alt/PredictorAltPorts_LiqScreen_VWforce.parquet'),
    'quintiles_ew': 'Portfolios/Full Sets Alt/PredictorAltPorts_Quintiles.parquet',
    'quintiles_vw': 'Portfolios/Full Sets Alt/PredictorAltPorts_QuintilesVW.parquet',
    'ff93': 'Portfolios/Full Sets Alt/PredictorAltPorts_FF93style.parquet',
    'holdper1': 'Portfolios/Full Sets Alt/PredictorAltPorts_HoldPer_1.parquet',
    'holdper3': 'Portfolios/Full Sets Alt/PredictorAltPorts_HoldPer_3.parquet',
    'holdper6': 'Portfolios/Full Sets Alt/PredictorAltPorts_HoldPer_6.parquet',
    'holdper12': 'Portfolios/Full Sets Alt/PredictorAltPorts_HoldPer_12.parquet',
    # Daily portfolios
    'daily_op_ew': 'DailyPortfolios/Predictor.parquet',
    'daily_op_vw': 'DailyPortfolios/PredictorVW.parquet',
    'daily_deciles_ew': 'DailyPortfolios/CtsPredictorDecile.parquet',
    'daily_deciles_vw': 'DailyPortfolios/CtsPredictorDecileVW.parquet',
    'daily_quintiles_ew': 'DailyPortfolios/CtsPredictorQuintile.parquet',
    'daily_quintiles_vw': 'DailyPortfolios/CtsPredictorQuintileVW.parquet',
}


def _get_hf_url(url_prefix, revision, path):
    return f'{url_prefix}/{quote(revision, safe="")}/{quote(path)}'


def _get_hf_name_id_map(url_prefix, revision):
    # Same columns as the Google Drive map: name, full_name, file_id,
    # download_name
    return pl.DataFrame(
        {
            'name': [i.split('/')[-1] for i in HF_DATASETS.values()],
            'full_name': list(HF_DATASETS.values()),
            'file_id': [
                _get_hf_url(url_prefix, revision, i)
                for i in HF_DATASETS.values()],
            'download_name': list(HF_DATASETS.keys()),
        }
    )
