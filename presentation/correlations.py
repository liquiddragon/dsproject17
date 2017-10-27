import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

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

# Add human readable labels to the features:
feature_labels = ['Capital Formation',
       'Imports',
       'Immigration',
       'Pupil/Teacher Ratio',
       'Infant Mortality',
       'Foreign Trade',
       'Rural Population',
       'Fertility Rate',
        'Life Expectancy / Male',
       'Life Expectancy / Female',
       'Ages 65 and Older',
       'Age Dependency Ratio', 'Young Pregnancies',
       'Deaths per 1000',
       'Population',
       'Life Expectancy',
       'Exports',
       'Births per 1000', 'Democracy Score',
       'Government Spending', 'Surface Area',
       'Per Capita Fat Supply',
       'Per Capita Protein Supply',
       'CO^2 Emissions',
       'Military Expenditure',
       'CO^2 Emissions International',
       'Per Capita Calorie Supply',
       'Foor Imports',
       'Agricultural Products Imports',
       'Food Exports',
       'Agricultural Products Exports']

importances['feature_name'] = feature_labels

importances.to_csv('presentation/correlation_analysis.csv')

# Export images:

num = len(importances['importance'])

importance_values = importances['importance'].values
feature_names = importances['feature_name'].copy().values

#insert new lines for strings that are too long
cutoff = 5
for idx, nam in enumerate(feature_names):
    if len(nam) > cutoff :
        spaces = np.array([x.start() for x in re.finditer(' ', nam)])
        if len(spaces[spaces > cutoff])>0: #if we found a space
            pos = spaces[spaces > cutoff][0] #get first space
            feature_names[idx] = nam[:pos] + '\n' + nam[pos:]

values = [importance_values[:num//2], importance_values[num//2:]]
names = [feature_names[:num//2], feature_names[num//2:]]

fig, axs = plt.subplots(nrows=2, sharey=True, figsize=(25,18), dpi=40)

_ = fig.suptitle('Effects on GDP growth',
          **{'family': 'Arial Black', 'size': 40, 'weight': 'bold'})

# Generete feature importances plot
for i in range(2):
    _ = axs[i].bar(range(len(values[i])), values[i], align='center', color='orange')
    _ = axs[i].set_xticks(range(len(names[i])))
    _ = axs[i].set_xticklabels(names[i], rotation='vertical')
    _ = axs[i].set_xlim(-1, len(names[i]))
    _ = axs[i].tick_params(axis='x', labelsize=28)
    _ = axs[i].tick_params(axis='y', labelsize=28)

fig.subplots_adjust(bottom=0.15, top=0.95, hspace=0.8)

plt.savefig('presentation/images/importances.png',bbox_inches='tight')
plt.show()

fig, axs = plt.subplots(nrows=2, sharey=True, figsize=(25,18), dpi=40)

_ = fig.suptitle('Feature Correlation to Growth',
          **{'family': 'Arial Black', 'size': 40, 'weight': 'bold'})

correlation_values = importances['corr_to_growth'].values
values = [correlation_values[:num//2], correlation_values[num//2:]]

# Generate correlations plot
for i in range(2):
    _ = axs[i].bar(range(len(values[i])), values[i], align='center', color='brown')
    _ = axs[i].set_xticks(range(len(names[i])))
    _ = axs[i].set_xticklabels(names[i], rotation='vertical')
    _ = axs[i].set_xlim(-1, len(names[i]))
    _ = axs[i].tick_params(axis='x', labelsize=28)
    _ = axs[i].tick_params(axis='y', labelsize=28)

fig.subplots_adjust(bottom=0.15, top=0.95, hspace=0.8)

plt.savefig('presentation/images/correlations.png',bbox_inches='tight')
plt.show()

