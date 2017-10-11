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
    '''Create filename based on item and element names'''
    fname = item.lower().strip().translate({ord(c): None for c in string.punctuation})
    fname += '-' + element.lower().strip().translate({ord(c): None for c in string.punctuation})
    fname = fname.replace(' ', '_')
    fname += '.csv'
    return fname

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
with open('Production_Crops_E_All_Data.csv', 'r', newline='', encoding='ISO-8859-1') as csvIn:
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

        # Items are at position 3 with example of 'Almonds, with shell'
        if row[3] not in items:
            items[row[3]] = {}
        # Elements are at position 5 with example of 'Production'
        if row[5] not in items[row[3]]:
            items[row[3]][row[5]] = {}
        # Country names are at position 1 with example of 'Albania'
        if row[1] not in items[row[3]][row[5]] and row[1] not in extra_columns:
            items[row[3]][row[5]][row[1]] = []
            odd = True
            # Values are from position 7 onwards according to year on every other spot
            # E.g. column header of 7 is 1961 and its value 16610.000000
            # Those other spots contain a flag as per description
            for item in row[7:]:
                if odd:
                    num = strToFloat(item)
                    items[row[3]][row[5]][row[1]].append(num)
                    odd = False
                else:
                    odd = True

print('Writing...')

# Create index labels for dataframes
index_labels = []
for i in range(start_year, end_year + 1):
    index_labels.append(i)

# Process all entries and create dataframes, which are then saved to individual
# CSV files
for item in items:
    for element in items[item]:
        df = pd.DataFrame()
        for country in items[item][element]:
            df[country] = items[item][element][country]
        df.index = index_labels
        df.to_csv(get_filename(item, element))
