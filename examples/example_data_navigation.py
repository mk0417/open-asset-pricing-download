################################
### Example to navigate data ###
################################


#%%
#pip show <openassetpricing>

#%pip install -U openassetpricing

pip install .
# %%
# Set Up
import openassetpricing as oap
import pandas as pd
import numpy as np

# Initialize OpenAP
openap = oap.OpenAP()

#%% Test: pull yearly release
# Set Up
import openassetpricing as oap
import pandas as pd
import numpy as np
openap = oap.OpenAP('2024')

#%%
# List available datasets
openap.list_datasets()

#%%
# Download port_op series
df = openap.dl('port_op', 'pandas')
df.head()

# %% 
# 1. Check how investment predictors have done in past 10 years: 
# 1.1 Use Signal_doc to find investment predictors
df1 = openap.dl('signal_doc', 'pandas')

# Filter for Predictor Signals
df_predictor = df1[(df1["Cat.Signal"] == "Predictor")]

# Look for "Investment" in "Detailed Definition"
search_term = "investment"
bool_vector = pd.Series(df_predictor["Detailed Definition"]).str.contains(search_term).tolist()
true_indices2 = np.where(bool_vector)[0]

# Keep only investment predictors
df_predictor = df_predictor.iloc[true_indices2]

# Key characteristics of investment predictors
invest_pred = df_predictor[["Acronym", "Authors", "Year", "Journal"]].copy()
invest_pred

# Extract names of investment predictors
invest_pred_names = df_predictor["Acronym"].tolist()

# %% 
# 1.2 Combine Signal_doc with returns dataset to calculate average returns
# Filter for investment predictors in returns dataset
df2 = openap.dl('port_op', 'pandas')
filtered_df2 = df2[df2["signalname"].isin(invest_pred_names)]

# Filter for last 10 years
filtered_df2["date"] = pd.to_datetime(filtered_df2["date"])
filter_date = '2014-01-01'
filtered_df2 = filtered_df2[filtered_df2["date"] >= filter_date]

# Calculate average returns 
invest_pred_returns = filtered_df2.groupby('signalname')["ret"].mean()
print(invest_pred_returns)

# %%
# 2. Choose a liquidity screen and see how portfolios have done
df3 = openap.dl('port_nyse', 'pandas')
nyse_mean_returns = df3.groupby('signalname')["ret"].mean()
print(nyse_mean_returns)

# %%
