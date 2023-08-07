import pickle
from datetime import timedelta
import itertools
import pandas as pd
from cluster_the_data import preprocess_data as ps


input_file = 'data_dict.pickle'  # File path of the pickle file
with open(input_file, 'rb') as f:
    loaded_dict = pickle.load(f)
keys_to_keep = ['heart_rate_daily','light_sleep','awake_sleep','deep_sleep','epoch',"dailies_summary"]
filtered_data = {key: loaded_dict[key] for key in keys_to_keep if key in loaded_dict}
ps(filtered_data)


