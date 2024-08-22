###################
### Test README
###################

#%%
# Set Up

import openassetpricing as oap

# Initialize OpenAP
openap = oap.OpenAP()

# ==========
# List available datasets
# ==========
openap.list_datasets()

#%%
### Download list of predictors
# Use Polars dataframe
df = openap.dl('signal_doc', 'polars')

# Use Pandas dataframe
df = openap.dl('signal_doc', 'pandas')

#%%
### Download portfolio returns
#### Download all predictors

# Download OP portfolio returns in Polars dataframe
df = openap.dl('port_op', 'polars')

# Download equal-weighted decile portfolio returns in Pandas dataframe
df = openap.dl('port_deciles_ew', 'pandas')

#%%
#### Download specific predictors

# Download BM portfolio returns based on NYSE stocks only in Polars dataframe
df = openap.dl('port_nyse', 'polars', ['BM'])
# Download BM and 12-month momentum value-weighted
# quintile portfolio returns in Polars dataframe
df = openap.dl('port_quintiles_vw', 'polars', ['BM', 'Mom12m'])

# Use Pandas dataframe
df = openap.dl('port_nyse', 'pandas', ['BM'])
df = openap.dl('port_quintiles_vw', 'pandas', ['BM', 'Mom12m'])

#%%
### Download firm characteristics
#### Download all firm characteristics

# Use Polars dataframe
df = openap.dl('char_predictors', 'polars')

#%%
# Use Pandas dataframe
df = openap.dl('char_predictors', 'pandas')

#%%
# #### Download specific firm characteristics

# Use Polars dataframe
df = openap.dl('char_predictors', 'polars', ['BM'])
df = openap.dl('char_predictors', 'polars', ['BM', 'Mom12m'])

# Use Pandas dataframe
df = openap.dl('char_predictors', 'pandas', ['BM'])
df = openap.dl('char_predictors', 'pandas', ['BM', 'Mom12m'])

#%%
###################
### goal: example that downloads predictor data related to "duration"
###################

#%%
# Look around 

# download signal_doc
df = openap.dl('signal_doc', 'pandas')
df.head()
df

# %%
df_predictor = df[(df["Cat.Signal"] == "Predictor")]

# %%
import pandas as pd
import numpy as np

# %% Looking for "duration" in "LongDescription"
bool_vector = pd.Series(df_predictor["LongDescription"]).str.contains('Duration').tolist()
true_indices1= np.where(bool_vector)[0]
true_indices1 # Duration apears in row 62 
df_predictor.loc[62, "LongDescription"]

# %% Looking for "duration" in "Detailed Definition"
search_term = "investment"
bool_vector = pd.Series(df_predictor["Detailed Definition"]).str.contains(search_term).tolist()
true_indices2 = np.where(bool_vector)[0]
true_indices2 # duration appears in row 205
#df_predictor.loc[205,"Detailed Definition"]

# %% Looking for "time" in "Detailed Definition"
bool_vector = pd.Series(df_predictor["Detailed Definition"]).str.contains('time ').tolist()
true_indices3 = np.where(bool_vector)[0]
true_indices3 # time appears in row 211
df_predictor.loc[211,"Detailed Definition"] 

# %% Looking for "month" in "Detailed Definition"
bool_vector = pd.Series(df_predictor["Detailed Definition"]).str.contains('month').tolist()
true_indices4 = np.where(bool_vector)[0] #appears many times
true_indices4

# %% Looking for "year" in "Detailed Definition"
bool_vector = pd.Series(df_predictor["Detailed Definition"]).str.contains('year').tolist()
true_indices5 = np.where(bool_vector)[0] #appears many times 
true_indices5 

# %% Looking for " age" in "Detailed Definition"
bool_vector = pd.Series(df_predictor["Detailed Definition"]).str.contains(' age').tolist()
true_indices6 = np.where(bool_vector)[0] #appears many times 
true_indices6 

# %% Looking for "term" in "Detailed Definition"
bool_vector = pd.Series(df_predictor["Detailed Definition"]).str.contains('term').tolist()
true_indices7 = np.where(bool_vector)[0] #appears many times 
true_indices7 

# %% Combine arrays to have all rows related to "duration"
true_indices = np.concatenate((true_indices1, true_indices2, true_indices3, true_indices4, true_indices5, true_indices6, true_indices7))
true_indices = np.unique(true_indices)

df_final = df_predictor.iloc[true_indices]
df_final

# %%
