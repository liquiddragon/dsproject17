import pandas as pd
import numpy as np

# Load feature importance matrix:
importances = pd.read_csv('presentation/feature_importances.csv', index_col=0)
importances['corr_to_growth'] = np.nan

# Load training data we used for training:
training_set = pd.read_csv('ml/training/data_interpolated.csv', index_col=0)

# Perform correlation analysis between each feature and GDP growth in 15 years:

for i in importances.index.values:
    feature = importances.loc[i]['feature']
    corr = training_set[feature].corr(training_set['gdp_in_15_years'])
    importances.loc[i, 'corr_to_growth'] = corr

importances.to_csv('presentation/correlation_analysis.csv')

