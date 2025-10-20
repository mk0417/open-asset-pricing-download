import openassetpricing as oap


# List available release versions
oap.list_release()

# Initialize OpenAP with most recent release
openap = oap.OpenAP()

# ==========
# List available portfolios
# ==========
openap.list_port()



# ==========
# Download SignalDoc.csv in pandas dataframe
# ==========
df = openap.dl_signal_doc('pandas')



# ==========
# Portfolios -> Full Sets OP -> PredictorPortsFull.csv
# ==========

# Download entier file in polars dataframe
df = openap.dl_port('op', 'polars')

# Download specific predictors (can be single or multiple predictors)
df = openap.dl_port('op', 'polars', ['AM'])
df = openap.dl_port('op', 'polars', ['AM', 'Mom12m'])



# ==========
# Portfolios -> Full Sets Alt -> PredictorAltPorts_Deciles.zip
# Portfolios -> Full Sets Alt -> PredictorAltPorts_DecilesVW.zip
# Portfolios -> Full Sets Alt -> PredictorAltPorts_LiqScreen_NYSEonly.zip
# ==========

# Download entier file
df = openap.dl_port('deciles_ew', 'polars')
df = openap.dl_port('deciles_vw', 'polars')
df = openap.dl_port('nyse', 'pandas')

# Download specific predictors (can be single or multiple predictors)
df = openap.dl_port('deciles_ew', 'polars', ['Accruals'])
df = openap.dl_port('deciles_ew', 'polars', ['BM', 'Mom6m'])



# ==========
# Firm Level Characteristics
# ==========

# Download all firm characteristics (signed)
df = openap.dl_all_signals('polars')

# Download specific firm characteristics
df = openap.dl_signal('polars', ['BM'])
