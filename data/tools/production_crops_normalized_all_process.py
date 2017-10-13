import csv
import pandas as pd
import string

extra_columns = ['Net Food Importing Developing Countries','South America',
    'Low Income Food Deficit Countries','Caribbean','World','Southern Europe','Middle Africa',
    'European Union','Asia','Europe','Americas','Central America','South-Eastern Asia',
    'Small Island Developing States','Western Europe','Northern America','South America',
    'Land Locked Developing Countries','Southern Africa','Southern Asia','Northern Africa',
    'Least Developed Countries','European Union','Africa','Western Asia','Eastern Asia',
    'Americas','Eastern Europe','Central Asia','Western Africa','Oceania','Northern America',
    'Eastern Africa','Northern Europe']

def get_filename(item, element):
    fname = item.lower().strip().translate({ord(c): None for c in string.punctuation})
    fname += '-' + element.lower().strip().translate({ord(c): None for c in string.punctuation})
    fname = fname.replace(' ', '_')
    fname += '_normalized.csv'
    return fname

def strToInt(value):
    try:
        number = int(value)
    except ValueError:
        number = -1
    return number

def strToFloat(value):
    try:
        number = float(value)
    except ValueError:
        number = -1
    return number

header = False
start_year = 1961
end_year = 2014
items = {}
print('Reading...')
with open('Production_Crops_E_All_Data_(Normalized).csv', 'r', newline='', encoding='ISO-8859-1') as csvIn:
    item_reader = csv.reader(csvIn, delimiter=',')
    for row in item_reader:
        if header == False:
            header = True
            continue

        if row[3] not in items:
            #print('Item: ' + row[3])
            items[row[3]] = {}
        if row[5] not in items[row[3]]:
            #print('  Element: ' + row[5])
            items[row[3]][row[5]] = {}
        if row[1] not in items[row[3]][row[5]] and row[1] not in extra_columns:
            #print('    Country: ' + row[1])
            items[row[3]][row[5]][row[1]] = {}

        if row[1] not in extra_columns:
            year = strToInt(row[7])
            value = strToFloat(row[9])
            items[row[3]][row[5]][row[1]][year] = value

print('Writing...')
index_labels = []
for i in range(start_year, end_year + 1):
    index_labels.append(i)

for item in items:
    for element in items[item]:
        df = pd.DataFrame(index=index_labels)
        for country in items[item][element]:
            for year,value in items[item][element][country].items():
                df.at[year, country] = value
        df.to_csv(get_filename(item, element))
