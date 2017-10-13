import argparse
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
    'Eastern Africa','Northern Europe','Sub-Saharan Africa','UK, poor workers',
    'England, farm laborers','England, all','Euro area','Low & middle income',
    'Heavily indebted poor countries (HIPC)','Least developed countries: UN classification',
    'High income','Pacific island small states','Post-demographic dividend',
    'Europe & Central Asia (IDA & IBRD)','Early-demographic dividend',
    'Sub-Saharan Africa (IDA & IBRD','Latin America & Caribbean (IDA & IBRD)',
    'Europe & Central Asia (excluding high income)','IDA blend','IDA only','Low income',
    'Middle East & North Africa (IDA & IBRD)','Latin America & Caribbean',
    'Pre-demographic dividend','Other small states','IBRD only',
    'Sub-Saharan Africa (excluding high income)','IDA total',
    'Fragile and conflict affected situations','Latin America & Caribbean (excluding high income)',
    'East Asia & Pacific (IDA & IBRD)','Middle East & North Africa','Europe & Central Asia',
    'East Asia & Pacific','Central Europe and the Baltics','Arab World','Lower middle income',
    'IDA & IBRD total','Small states','Caribbean small states',
    'East Asia & Pacific (excluding high income)','Late-demographic dividend',
    'Upper middle income','South Asia (IDA & IBRD)',
    'Middle East & North Africa (excluding high income)','OECD members','Middle income']

def strToInt(value):
    '''Convert string to integer value'''
    try:
        number = int(value)
    except ValueError:
        number = -1
    return number

def strToFloat(value):
    '''Convert string to floating point value'''
    try:
        number = float(value)
    except ValueError:
        number = -1
    return number

def main(infile, outfile, country_index, year_index, value_index, percent_value):
    header = False
    start_year = -1
    end_year = -1
    pdata = {}
    largest_value = -1

    print('Reading...')
    with open(infile, 'r', newline='', encoding='ISO-8859-1') as csvIn:
        item_reader = csv.reader(csvIn, delimiter=',')
        for row in item_reader:
            if header == False:
                header = True

            if row[country_index] not in extra_columns and row[country_index] not in pdata:
                pdata[row[country_index]] = {}

            if row[country_index] not in extra_columns:
                year_value = strToInt(row[year_index])
                if start_year == -1: start_year = year_value
                if year_value < start_year: start_year = year_value
                if end_year == -1: end_year = year_value
                if year_value > end_year: end_year = year_value
                # Skip unknown year values
                if year_value > 0:
                    if percent_value == True:
                        val = strToFloat(row[value_index])
                        if val > largest_value: largest_value = val
                    pdata[row[country_index]][year_value] = strToFloat(row[value_index])

    print('Writing...')

    # Create index labels for dataframes
    index_labels = []
    for i in range(start_year, end_year):
        index_labels.append(i)

    # Create dataframe with all information combined and store it
    df = pd.DataFrame(index=index_labels)
    for country in pdata:
        for year, value in pdata[country].items():
            if value == -1 or value == 0:
                value = np.nan
            df.at[year, country] = value

    df.to_csv(outfile)

    # Normalize data and store it
    if percent_value == False:
        df = df.div(df.sum(axis=1), axis=0)
    else:
        if largest_value <= 100:
            df = df / 100
        else:
            df = df / 1000
    normalized_outfile = outfile[:outfile.find('.csv')] + "_normalized" + outfile[outfile.find('.csv'):]
    df.to_csv(normalized_outfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', action='store', type=str, help='input filename')
    parser.add_argument('country', action='store', type=int, help='country column index')
    parser.add_argument('year', action='store', type=int, help='year column index')
    parser.add_argument('value', action='store', type=int, help='value column index')
    parser.add_argument('outfile', action='store', type=str, help='output filename')
    parser.add_argument('-p', '--percent', action='store_true', help='value is in percent')
    args = parser.parse_args()

    main(args.infile, args.outfile, args.country, args.year, args.value, args.percent)
