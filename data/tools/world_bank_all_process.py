import pandas as pd

# columns to remove:
#some countries which may need to be excluded, but not sure yet:
#['Bahamas, The', 'Aruba', 'Andorra', 'Channel Islands', 'Comoros',  'Faroe Islands',
#'Micronesia, Fed. Sts.', 'Gibraltar', 'Greenland',  'Isle of Man', 'St. Kitts and Nevis',
# 'St. Lucia',  'St. Martin (French part)', 'Palau', 'Marshall Islands', 'French Polynesia',
# 'Solomon Islands', 'San Marino', 'New Caledonia', 'Nauru', 'Northern Mariana Islands',
# 'Sao Tome and Principe', 'Sint Maarten (Dutch part)', 'Seychelles', 'Turks and Caicos Islands',
# 'St. Vincent and the Grenadines', 'British Virgin Islands', 'Virgin Islands (U.S.)', 'Vanuatu',
# 'Samoa', 'Kosovo', 'Tuvalu', 'Cabo Verde', 'Curacao', 'Cayman Islands',
exclude_countries = ['Palau', 'Monaco', 'Gibraltar', 'Nauru', 'American Samoa',
        'Saint Helena, Ascension and Tristan da Cunha', 'Dominica',
        'Montserrat', 'Wallis and Futuna Islands', 'Andorra',
        'St. Kitts and Nevis', 'Tokelau', 'Cook Islands', 'Isle of Man',
        'San Marino', 'Northern Mariana Islands', 'Holy See', 'Greenland',
        'Seychelles', 'Bermuda', 'Cayman Islands', 'Saint Pierre and Miquelon',
        'Anguilla', 'Antigua and Barbuda', 'Falkland Islands (Malvinas)',
        'Turks and Caicos Islands', 'Niue', 'Tuvalu', 'Faroe Islands',
        'Marshall Islands', 'Kiribati', 'British Virgin Islands',
        'Liechtenstein']

exclude_groups = [ 'Arab World', 'Central Europe and the Baltics', 'Caribbean small states',
        'East Asia & Pacific (excluding high income)', 'Early-demographic dividend',
        'East Asia & Pacific', 'Europe & Central Asia (excluding high income)',
        'Europe & Central Asia', 'Euro area', 'European Union',
        'Fragile and conflict affected situations', 'High income',
        'Heavily indebted poor countries (HIPC)', 'IBRD only', 'IDA & IBRD total',
        'IDA total', 'IDA blend', 'IDA only', 'Not classified',
        'Latin America & Caribbean (excluding high income)',
        'Latin America & Caribbean', 'Least developed countries: UN classification',
        'Low income', 'Lower middle income', 'Low & middle income', 'Late-demographic dividend',
        'Middle East & North Africa',  'Middle income',
        'Middle East & North Africa (excluding high income)',
        'North America', 'OECD members', 'Other small states',
        'Pre-demographic dividend', 'Pacific island small states',
        'Post-demographic dividend', 'Sub-Saharan Africa (excluding high income)',
        'Sub-Saharan Africa', 'Small states', 'South Asia',
        'East Asia & Pacific (IDA & IBRD countries)',
        'Europe & Central Asia (IDA & IBRD countries)',
        'Latin America & the Caribbean (IDA & IBRD countries)',
        'Middle East & North Africa (IDA & IBRD countries)', 'South Asia (IDA & IBRD)',
        'Sub-Saharan Africa (IDA & IBRD countries)',  'Upper middle income']

# process worldbank data
# source: path to raw data
# skiprows: how many of the rows to skip when reading the CSV
# drop1 : how many leading rows to remove from data
# drop2 : how many trailing rows to remove from data
# output : name of output data (without .csv extension)
# normalize : boolean, whether to output CSV normalized by World values
def worldbank_import(source, skiprows, drop1, drop2, output, normalize=False):
    df = pd.read_csv('../raw/worldbank/' + source + '/' + source + '.csv', skiprows=skiprows)
    # make years be on the vertical axis
    df = df.transpose()

    # set column names to countries
    df.columns = df.iloc[0].values

    # get rid of extra leading rows
    df = df.drop(df.index[0:drop1])

    # get rid of extra trailing rows
    if drop2:
        df = df.drop(df.index[drop2:])

    # get rid of columns we don't want
    for name in exclude_countries + exclude_groups :
        try :
            del df[name]
        except KeyError:
            print("Column %s not in this dataframe" % name)

    # write regular csv
    df.to_csv('../processed/' + output + '.csv')

    # write normalized file if wanted:
    if normalize:
        normdf = df.loc[:, df.columns != 'World'].div(df['World'].values, axis=0)
        normdf.to_csv('../processed/' + output + '_normalized.csv')

    return


data_files = [
    # GDP Per capita
    ['API_NY.GDP.PCAP.CD_DS2_en_csv_v2', 4, 4, -1, 'gdp_per_capita_current_usd', True],

    # Surface area
    ['API_AG.SRF.TOTL.K2_DS2_en_csv_v2', 3, 5, -1, 'surface_area_sq_km', False],

    # Exports of goods and services
    ['API_NE.EXP.GNFS.ZS_DS2_en_csv_v2', 3, 4, -1,
     'exports_of_goods_and_services_percentage_of_gdp', True],

    # Rural population percentage
    ['API_SP.RUR.TOTL.ZS_DS2_en_csv_v2', 3, 4, -1, 'rural_population_percentage', True],

    # Birth rate, crude (per 1,000 people)
    # https://data.worldbank.org/indicator/SP.DYN.CBRT.IN
    # API_SP.DYN.CBRT.IN_DS2_en_csv_v2
    ['API_SP.DYN.CBRT.IN_DS2_en_csv_v2', 3, 4, -2, 'births_per_1000', True],

    # Death rate, crude (per 1,000 people)
    # https://data.worldbank.org/indicator/SP.DYN.CDRT.IN
    # API_SP.DYN.CDRT.IN_DS2_en_csv_v2
    ['API_SP.DYN.CBRT.IN_DS2_en_csv_v2', 3, 4, -2, 'deaths_per_1000', True],

    # Life expectancy at birth, total (years)
    # https://data.worldbank.org/indicator/SP.DYN.LE00.IN
    # API_SP.DYN.LE00.IN_DS2_en_csv_v2
    ['API_SP.DYN.LE00.IN_DS2_en_csv_v2', 3, 4, -2, 'life_expectancy', True],

    # Life expectancy at birth, female (years)
    # https://data.worldbank.org/indicator/SP.DYN.LE00.FE.IN
    # API_SP.DYN.LE00.FE.IN_DS2_en_csv_v2
    ['API_SP.DYN.LE00.FE.IN_DS2_en_csv_v2', 3, 4, -2, 'life_expectancy_female', True],

    # Life expectancy at birth, male (years)
    # https://data.worldbank.org/indicator/SP.DYN.LE00.MA.IN
    # API_SP.DYN.LE00.MA.IN_DS2_en_csv_v2
    ['API_SP.DYN.LE00.MA.IN_DS2_en_csv_v2', 3, 4, -2, 'life_expectancy_male', True],

    # Mortality rate, infant (per 1,000 live births)
    # https://data.worldbank.org/indicator/SP.DYN.IMRT.IN
    # API_SP.DYN.IMRT.IN_DS2_en_csv_v2
    ['API_SP.DYN.IMRT.IN_DS2_en_csv_v2', 3, 4, -2, 'infant_mortality_per_1000', True],

    # Fertility rate, total (births per woman)
    # https://data.worldbank.org/indicator/SP.DYN.TFRT.IN
    # API_SP.DYN.TFRT.IN_DS2_en_csv_v2
    ['API_SP.DYN.TFRT.IN_DS2_en_csv_v2', 3, 4, -2, 'fertility_rate', True],

    # Age dependency ratio (% of working-age population)
    # https://data.worldbank.org/indicator/SP.POP.DPND
    # API_SP.POP.DPND_DS2_en_csv_v2
    ['API_SP.POP.DPND_DS2_en_csv_v2', 3, 4, -1, 'age_dependency_ratio', True],

    # Population ages 65 and above (% of total)
    # https://data.worldbank.org/indicator/SP.POP.65UP.TO.ZS
    # API_SP.POP.65UP.TO.ZS_DS2_en_csv_v2
    ['API_SP.POP.65UP.TO.ZS_DS2_en_csv_v2', 3, 4, -1, 'ages_65_and_older_percentage', True],

    # Gross capital formation (% of GDP)
    # https://data.worldbank.org/indicator/NE.GDI.TOTL.ZS
    # API_NE.GDI.TOTL.ZS_DS2_en_csv_v2
    ['API_NE.GDI.TOTL.ZS_DS2_en_csv_v2', 3, 4, -1, 'gross_capital_formation', True],

    # Adolescent fertility rate (births per 1,000 women ages 15-19)
    # https://data.worldbank.org/indicator/SP.ADO.TFRT
    # API_SP.ADO.TFRT_DS2_en_csv_v2
    ['API_SP.ADO.TFRT_DS2_en_csv_v2', 3, 4, -2, 'young_pregnancies', True],

    # Net migration
    # https://data.worldbank.org/indicator/SM.POP.NETM?view=chart
    # API_SM.POP.NETM_DS2_en_csv_v2
    # NA:s need to be filled
    # net migration needs to be normalized by population
    ['API_SM.POP.NETM_DS2_en_csv_v2', 3, 4, -1, 'net_migration', False],

    # Imports of goods and services (% of GDP)
    # https://data.worldbank.org/indicator/NE.IMP.GNFS.ZS?view=chart
    # API_NE.IMP.GNFS.ZS_DS2_en_csv_v2
    # Note: quite a lot of missing data
    ['API_NE.IMP.GNFS.ZS_DS2_en_csv_v2', 3, 4, -1,
     'imports_of_goods_and_services_percentage_of_gdp', True]

]

for d in data_files:
    worldbank_import(d[0], d[1], d[2], d[3], d[4], d[5])

