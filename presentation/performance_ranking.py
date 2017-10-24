import pandas as pd
import numpy as np

#load unnormalized gdp file

gdp = pd.read_csv('data/processed/interpolated/gdp_per_capita_current_usd_nh_ip.csv', index_col=0)

#get the values from 2015, remove NaNs
gdp_values = np.array(gdp.loc[2015].values).astype(np.double)
mask = np.isfinite(gdp_values)
gdp_vals_non_nan = gdp_values[mask]

#calculate the mean gdp/capita in 2015
gdp_mean = np.mean(gdp_vals_non_nan)

low = gdp.loc[2015][gdp.loc[2015] < gdp_mean] # values below the mean
high = gdp.loc[2015][gdp.loc[2015] >= gdp_mean] # values above the mean

high_income_countries = high.index.values
low_income_countries = low.index.values

# get country names
high_income_countries = high.index.values
low_income_countries = low.index.values

# load our predictions
predictions_all = pd.read_csv('presentation/predictions.csv', index_col=0)

# we only care about 2030
predictions = predictions_all.loc[2030]

pred_mean = np.mean(predictions_all.loc[2030])
pred_std = np.std(predictions_all.loc[2030])

# convert predictions to "normalized" values

predictions = (predictions-pred_mean)/pred_std

# predictions for high and low income countries correspondingly:
high_predictions = predictions.loc[high_income_countries]
low_predictions = predictions.loc[low_income_countries]


top_performers_low_income = low_predictions.sort_values(ascending=False)[0:20]
bottom_performers_low_income = low_predictions.sort_values(ascending=False)[-20:]

top_performers_high_income = high_predictions.sort_values(ascending=False)[0:20]
bottom_performers_high_income = high_predictions.sort_values(ascending=False)[-20:]

top_performers_low_income.to_csv('presentation/top_performers_low_income.csv')
bottom_performers_low_income.to_csv('presentation/bottom_performers_low_income.csv')
top_performers_high_income.to_csv('presentation/top_performers_high_income.csv')
bottom_performers_high_income.to_csv('presentation/bottom_performers_high_income.csv')
