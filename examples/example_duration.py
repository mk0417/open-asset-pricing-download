# goal: example that downloads predictor data related to "duration"

#%%
# Setup

import openassetpricing as oap

# Initialize OpenAP
openap = oap.OpenAP()

# ==========
# List available datasets
# ==========
openap.list_datasets()

# download signal_doc
df = openap.dl('signal_doc', 'pandas')

#%%
# Look around 

df.head()