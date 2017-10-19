import pandas as pd
import glob
import replacements
import sys
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Column names that are excluded from output
exclude_columns_list = ['Net Food Importing Developing Countries','South America',
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
    'Sub-Saharan Africa (IDA & IBRD)','Latin America & Caribbean (IDA & IBRD)',
    'Europe & Central Asia (excluding high income)','IDA blend','IDA only','Low income',
    'Middle East & North Africa (IDA & IBRD)','Latin America & Caribbean',
    'Pre-demographic dividend','Other small states','IBRD only','North America',
    'Sub-Saharan Africa (excluding high income)','IDA total','Channel Islands',
    'Fragile and conflict affected situations','Latin America & Caribbean (excluding high income)',
    'East Asia & Pacific (IDA & IBRD)','Middle East & North Africa','Europe & Central Asia',
    'East Asia & Pacific','Central Europe and the Baltics','Arab World','Lower middle income',
    'IDA & IBRD total','Small states','Caribbean small states','Melanesia',
    'East Asia & Pacific (excluding high income)','Late-demographic dividend',
    'Upper middle income','South Asia (IDA & IBRD)', 'South Asia','Holy See',
    'Middle East & North Africa (excluding high income)','OECD members','Middle income',
    'Latin America & Caribbean (all income levels)','Sub-Saharan Africa (all income levels)',
    'East Asia & Pacific (developing only)','High income: OECD','Sub-Saharan Africa (developing only)',
    'Latin America & Caribbean (developing only)','Middle East & North Africa (all income levels)',
    'East Asia & Pacific (all income levels)','Middle East & North Africa (developing only)',
    'Europe & Central Asia (developing only)','Europe & Central Asia (all income levels)',
    'West Bank and Gaza','World','Zanzibar','Occupied Palestinian Territory',
    'Pacific Islands Trust Territory','U.S. Territories','Hawaiian Trade Zone',
    'Education - Pupil-teacher ratio in primary education (headcount basis)',
    'U.S. Pacific Islands']

# Harmonize certain names before mapping attempt
replace_names = {
        'Micronesia (country)': 'Micronesia, Federated States of',
        'Macao': 'Macau',
        'Lao PDR': 'Laos',
        'St. Lucia': 'Saint Lucia',
        'Korea, Rep.': 'South Korea',
        'Kyrgyz Republic': 'Kyrgyzstan',
        'Korea, Dem. People’s Rep.': 'North Korea',
        'St. Martin (French part)': 'Saint-Martin (France)',
        'Micronesia, Fed. Sts.': 'Micronesia, Federated States of',
        'Cabo Verde': 'Cape Verde',
        "Democratic People's Republic of Korea": 'North Korea',
        'Republic of Korea': 'South Korea',
        'Burma': 'Myanmar',
        'Czechia': 'Czech Republic',
        'Netherlands Antilles (former)': 'Netherlands Antilles',
        'Yugoslav SFR': 'Yugoslavia',
        'Saint Pierre/Miquelon': 'Saint Pierre and Miquelon',
        'Korea, DPR': 'North Korea',
        'Former U.S.S.R.': 'Soviet Union',
        'Former Yugoslavia': 'Yugoslavia',
        'United States Virgin Islands': 'Virgin Islands, US'
        }

# Exclusion and mapping have issues with former countries and certain
# names, thus they are handled here
special_mappings = {
        'Yugoslavia': 'Yugoslavia',
        'Slovak Republic': 'Slovak Republic',
        'Netherlands Antilles': 'Netherlands Antilles',
        'Palestinian Territories': 'Palestinian Territories',
        'Laos': "Lao People's Democratic Republic",
        'USSR': 'Soviet Union'
        }

# Countries that are excluded from final data due to population size being
# below 100000
exclude_countries = ['Palau', 'Monaco', 'Gibraltar', 'Nauru', 'American Samoa',
        'Saint Helena, Ascension and Tristan da Cunha', 'Dominica',
        'Montserrat', 'Wallis and Futuna Islands', 'Andorra',
        'St. Kitts and Nevis', 'Tokelau', 'Cook Islands', 'Isle of Man',
        'San Marino', 'Northern Mariana Islands', 'Holy See', 'Greenland',
        'Seychelles', 'Bermuda', 'Cayman Islands', 'Saint Pierre and Miquelon',
        'Anguilla', 'Antigua and Barbuda', 'Falkland Islands (Malvinas)',
        'Turks and Caicos Islands', 'Niue', 'Tuvalu', 'Faroe Islands',
        'Marshall Islands', 'Kiribati', 'British Virgin Islands',
        'Virgin Islands, British', 'Liechtenstein', 'Germany East',
        'Kosovo', 'Vietnam South', 'Yemen South', 'Bonaire', 'Wake Island']

# Read list of countries and use their English names
country_file_name = 'countries.csv'
if not os.path.exists(country_file_name):
	print('File containing country names is missing')
	sys.exit(0)
countries = pd.read_csv(country_file_name, encoding='ISO-8859-1')
country_list = countries['English Name'].tolist()
country_list.sort()

# Process only those files that are normalized based on that string in their filename
data_files_path = '<INSERT PATH TO DATA FILES HERE>'
if data_files_path.find('HERE') >= 0:
    print('You need to input correct path to processed files in the script file!')
    sys.exit(0)
file_list = glob.glob(data_files_path + '/*normalized*')
# Add exceptional files to be processed
file_list.append(data_files_path + '/surface_area_sq_km.csv')
file_list.append(data_files_path + '/pupil-teacher_ratio_processed.csv')
file_list.append(data_files_path + '/net_migration.csv')
file_list.append(data_files_path + '/gdp_per_capita_current_usd.csv')
# Finally eliminate files containing word 'selected'
file_list = [entry for entry in file_list if entry.find('selected') < 0]

for filename in file_list:
    sfilename = filename[filename.rfind('/')+1:filename.find('.csv')]
    print('Processing ' + sfilename)

    # Read CSV file, remove duplicate columns and extract only column names
    df = pd.read_csv(filename, index_col=0)
    df = df.T.drop_duplicates().T
    df_countries_list = df.columns.values

    # Create mapping table from old name (as key) to new name (as value)
    mappings = {}
    for dfcn in df_countries_list:
        # Perform certain harmonization
        if dfcn in replace_names.keys():
            cname = replace_names[dfcn]
        else:
            cname = dfcn

        # Search for the one match from country list
        candidate = process.extractOne(cname, country_list)
        if candidate[1] < 80:
            mappings[dfcn] = candidate[0] + ' (' + str(candidate[1]) + ')'
        else:
            mappings[dfcn] = candidate[0]

    # Process mapping values
    remove_keys = []
    for k in mappings.keys():
        # Correct certain special cases
        if k in special_mappings.keys():
            mappings[k] = special_mappings[k]

        # Exclude certain column values
        if k in exclude_columns_list or k in exclude_countries or k.lower().find('unnamed') >= 0:
            remove_keys.append(k)

    # Remove selected columns from mappings dictionary
    for k in remove_keys:
        del mappings[k]

    # Collected columns to be removed from dataframe
    remove_keys.clear()
    for colname in df.columns.values:
        if colname not in mappings.keys():
            remove_keys.append(colname)
    remove_keys = list(set(remove_keys))

    # Remove selected columns
    for k in remove_keys:
        if k in df.columns.values:
            del df[k]

    # Write new column names in place and write dataframe to file
    df.rename(columns=mappings)
    df.to_csv('output/' + sfilename + '_nh.csv')
