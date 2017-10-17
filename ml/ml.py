import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor

"""initial testing"""

df = pd.read_csv("dsproject17/ml/training/data.csv")

# target
y = df.gdp_in_15_years
df.drop("gdp_in_15_years", axis=1, inplace=True)
df.drop("Unnamed: 0", axis=1, inplace=True)

# remove column names & convert to ndarray
df = np.asarray(df)
y = np.asarray(y)

# remove "micronesia" strings
df[1829:1860, 26] = np.nan

# remove nans
df = np.nan_to_num(df.astype(float))
y = np.nan_to_num(y.astype(float))

# training & test sets
X_train, X_test, y_train, y_test = \
    train_test_split(df, y, test_size=0.2)

# apply extra tree regressor
etr = ExtraTreesRegressor(n_estimators=40)
etr.fit(X_train, y_train)
print(etr.score(X_test, y_test))

