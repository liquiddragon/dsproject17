import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor
import matplotlib.pyplot as plt
from treeinterpreter import treeinterpreter

df = pd.read_csv("dsproject17/ml/training/data_interpolated.csv")
features = df.columns.values[1:-1]

# target
y = df.gdp_in_15_years
df.drop("gdp_in_15_years", axis=1, inplace=True)
df.drop("Unnamed: 0", axis=1, inplace=True)

# remove column names & convert to ndarray
df = np.asarray(df)
y = np.asarray(y)

# remove rows that contain no gdp information
ind = np.where(~np.isnan(y))[0]
y = y[ind]
df = df[ind, :]

# remove nans
df = np.nan_to_num(df.astype(float))
y = np.nan_to_num(y.astype(float))

# training & test sets
X_train, X_test, y_train, y_test = \
    train_test_split(df, y, test_size=0.2, random_state=123)

# apply extra tree regressor
etr = ExtraTreesRegressor(n_estimators=60, max_features="log2", random_state=1234)
etr.fit(X_train, y_train)
print(etr.score(X_test, y_test))

# predict future gdps
# load new data
data = pd.read_csv("dsproject17/ml/training/data_up_till_now_interpolated.csv")
data.drop("gdp_per_capita", axis=1, inplace=True)

# correct year numbering
names = data["Unnamed: 0"]
names = list(names)
for i in range(len(names)):
    names[i] = names[i][:-4] + str((int(names[i][-4:]) + 15))

# save results
data = np.asarray(data)
data = np.nan_to_num(data[:, 1:].astype(float))
etr.set_params(warm_start=True, n_estimators=72)
etr.fit(df, y)
predictions = etr.predict(data)
unique_names = pd.unique(np.asarray([n[:-7] for n in names]))
t = predictions.reshape(15, len(unique_names), order="F")
data = pd.DataFrame(data=t, index=np.arange(2016, 2031), columns=unique_names)
data.to_csv("dsproject17/presentation/predictions.csv")

# visualize test accuracy
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
fdf.to_csv("dsproject17/presentation/feature_importances.csv")

# feature contributions
_, _, con = treeinterpreter.predict(etr, X_test)
data = pd.DataFrame(data=con, index=np.arange(1115), columns=features)
data.to_csv("dsproject17/presentation/feature_contributions.csv")

# sums of feature conributions of each feature
f = np.sum(con, axis=0)
fio = np.column_stack((features[np.argsort(f)[::-1]], np.sort(f)[::-1]))
fdf = pd.DataFrame(fio)
fdf.columns = ["feature", "importance"]
fdf.to_csv("dsproject17/presentation/feature_contribution_sums.csv")

