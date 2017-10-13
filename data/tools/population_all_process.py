import csv
import pandas as pd
import numpy as np

extra_columns = ['Net Food Importing Developing Countries','South America',
    'Low Income Food Deficit Countries','Caribbean','World','Southern Europe','Middle Africa',
    'European Union','Asia','Europe','Americas','Central America','South-Eastern Asia',
    'Small Island Developing States','Western Europe','Northern America','South America',
    'Land Locked Developing Countries','Southern Africa','Southern Asia','Northern Africa',
    'Least Developed Countries','European Union','Africa','Western Asia','Eastern Asia',
    'Americas','Eastern Europe','Central Asia','Western Africa','Oceania','Northern America',
    'Eastern Africa','Northern Europe']

def strToFloat(value):
    '''Convert string to floating point value'''
    try:
        number = float(value)
    except ValueError:
        number = -1
    return number

# Main
header = False
start_year = -1
end_year = -1
items = {}

print('Reading...')
with open('Population_E_All_Data.csv', 'r', newline='', encoding='ISO-8859-1') as csvIn:
    item_reader = csv.reader(csvIn, delimiter=',')
    for row in item_reader:
        if header == False:
            header = True
            # Grab starting and ending years from the header row
            try:
                start_year = int(row[7][1:])
                end_year = int(row[len(row)-2][1:])
            except ValueError:
                start_year = -1
                end_year = -1
            continue

        # Country names are at position 1 with example of 'Albania' and
        # position 5 tells what population data is in question from which
        # only total population is chosen.
        if row[5] == "Total Population - Both sexes" and row[1] not in items and row[1] not in extra_columns:
            items[row[1]] = []
            odd = True
            # Values are from position 7 onwards according to year on every other spot
            # E.g. column header of 7 is 1950 and its value 7752.120000. Unit is 1000.
            # Those other spots contain a flag as per description
            for item in row[7:]:
                if odd:
                    num = strToFloat(item)
                    items[row[1]].append(num)
                    odd = False
                else:
                    odd = True

print('Writing...')

# Create index labels for dataframes
index_labels = []
for i in range(start_year, end_year + 1):
    index_labels.append(i)

# Create dataframe with all information combined and store it
df = pd.DataFrame()
for country in items:
    add_list = [x if x != -1 else np.nan for x in items[country]]
    df[country] = add_list

df.index = index_labels
df.to_csv('population_estimates_and_projections.csv')

# Normalize data and store it
df = df.div(df.sum(axis=1), axis=0)
df.to_csv('population_estimates_and_projections_normalized.csv')
