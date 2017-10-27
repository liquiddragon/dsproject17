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

predictions_normalized = (predictions-pred_mean)/pred_std

# predictions for high and low income countries correspondingly:
high_predictions = predictions.loc[high_income_countries]
low_predictions = predictions.loc[low_income_countries]

high_predictions_normalized = predictions_normalized.loc[high_income_countries]
low_predictions_normalized = predictions_normalized.loc[low_income_countries]

top_performers_low_income = low_predictions.sort_values(ascending=False)[0:20]
bottom_performers_low_income = low_predictions.sort_values(ascending=False)[-20:]

top_performers_low_income_normalized = low_predictions_normalized.sort_values(ascending=False)[0:20]
bottom_performers_low_income_normalized = low_predictions_normalized.sort_values(ascending=False)[-20:]

df_top_low = top_performers_low_income.to_frame('Velocity of Growth')
df_bottom_low = bottom_performers_low_income.to_frame('Velocity of Growth')

df_top_low['Normalized'] = top_performers_low_income_normalized
df_bottom_low['Normalized'] = bottom_performers_low_income_normalized

top_performers_high_income = high_predictions.sort_values(ascending=False)[0:20]
bottom_performers_high_income = high_predictions.sort_values(ascending=False)[-20:]

top_performers_high_income_normalized = high_predictions_normalized.sort_values(ascending=False)[0:20]
bottom_performers_high_income_normalized = high_predictions_normalized.sort_values(ascending=False)[-20:]

df_top_high = top_performers_high_income.to_frame('Velocity of Growth')
df_bottom_high = bottom_performers_high_income.to_frame('Velocity of Growth')

df_top_high['Normalized'] = top_performers_high_income_normalized
df_bottom_high['Normalized'] = bottom_performers_high_income_normalized

top_performers_low_income.to_csv('presentation/top_performers_low_income.csv')
bottom_performers_low_income.to_csv('presentation/bottom_performers_low_income.csv')
top_performers_high_income.to_csv('presentation/top_performers_high_income.csv')
bottom_performers_high_income.to_csv('presentation/bottom_performers_high_income.csv')

df_top_low.to_csv('presentation/top_performers_low_income_normalized.csv')
df_bottom_low.to_csv('presentation/bottom_performers_low_income_normalized.csv')
df_top_high.to_csv('presentation/top_performers_high_income_normalized.csv')
df_bottom_high.to_csv('presentation/bottom_performers_high_income_normalized.csv')
