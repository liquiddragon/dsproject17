import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor
import matplotlib.pyplot as plt

path = "dsproject17/ml/"
df = pd.read_csv(path + "training/data.csv")
features = df.columns.values[1:-1]

# target
y = df.gdp_in_15_years
df.drop("gdp_in_15_years", axis=1, inplace=True)
df.drop("Unnamed: 0", axis=1, inplace=True)

# remove column names & convert to ndarray
df = np.asarray(df)
y = np.asarray(y)

# remove "micronesia" strings
df[1829:1860, 26] = np.nan

# remove rows that contain no gdp information
ind = np.where(~np.isnan(y))[0]
y = y[ind]
df = df[ind, :]

# remove nans
df = np.nan_to_num(df.astype(float))
y = np.nan_to_num(y.astype(float))

# training & test sets
X_train, X_test, y_train, y_test = \
    train_test_split(df, y, test_size=0.2)

# apply extra tree regressor
etr = ExtraTreesRegressor(n_estimators=60, max_features="log2")
etr.fit(X_train, y_train)
print(etr.score(X_test, y_test))

# visualize results
res = etr.predict(X_test)
x = np.arange(len(y_test))
plt.plot(y_test, alpha=0.5, label="True values")
plt.plot(x, res, alpha=0.5, label="Predictions")
plt.legend(loc='upper right')
plt.show()

# feature importances
fi = etr.feature_importances_

# features ordered by importance
fio = np.column_stack((features[np.argsort(fi)[::-1]], np.sort(fi)[::-1]))
fdf = pd.DataFrame(fio)
fdf.columns = ["feature", "importance"]
fdf.to_csv(path + "feature_importances.csv")
