import pandas as pd
import numpy as np

df = pd.read_csv('../raw/unified_democracy_scores/uds_summary.csv')
df = df[['country', 'year', 'mean']]
df = df.pivot(index='year', columns='country', values='mean')
df = df.drop(df.index[0:14]) #get rid of years 1946-1959
del df.index.name
del df.columns.name

#TODO: Make sure that all our CSVs have the same countries
#countries that have pop below 100k
exclude_countries = ['Palau', 'Monaco', 'Gibraltar', 'Nauru', 'American Samoa',
       'Saint Helena, Ascension and Tristan da Cunha', 'Dominica',
       'Montserrat', 'Wallis and Futuna Islands', 'Andorra',
       'St. Kitts and Nevis', 'Tokelau', 'Cook Islands', 'Isle of Man',
       'San Marino', 'Northern Mariana Islands', 'Holy See', 'Greenland',
       'Seychelles', 'Bermuda', 'Cayman Islands', 'Saint Pierre and Miquelon',
       'Anguilla', 'Antigua and Barbuda', 'Falkland Islands (Malvinas)',
       'Turks and Caicos Islands', 'Niue', 'Tuvalu', 'Faroe Islands',
       'Marshall Islands', 'Kiribati', 'British Virgin Islands',
       'Liechtenstein', 'Germany East', 'Kosovo', 'Taiwan', 'Vietnam South',
       'Western Samoa', 'Yemen South']

#country names to replace
replace_names = {'Germany West': 'Germany',
                'Congo Brazzaville' : 'Congo, Rep.',
                'Congo Kinshasa': 'Congo, Dem. Rep.',
                'Myanmar (Burma)': 'Myanmar',
                'Russia (USSR)': 'Russian Federation',
                'Yugoslavia (Serbia)' : 'Serbia',
                'Vietnam North' : 'Vietnam',
                'Yemen North' : 'Yemen',
                'Bolivia (Plurinational State of)' : 'Bolivia',
                'China, Hong Kong SAR' : 'Hong Kong SAR, China',
                'China, Macao SAR' : 'Macao SAR, China',
                'Congo' : 'Congo, Rep.' ,
                'Czechia' : 'Czech Republic',
                "Côte d'Ivoire" : "Cote d'Ivoire",
                "Democratic People's Republic of Korea" : 'Korea, Dem. People’s Rep.',
                'Democratic Republic of the Congo' : 'Congo, Dem. Rep.',
                'Egypt' : 'Egypt, Arab Rep.',
                'Gambia' : 'Gambia, The',
                'Iran (Islamic Republic of)' : 'Iran, Islamic Rep.',
                'Kyrgyzstan' : 'Kyrgyz Republic',
                "Lao People's Democratic Republic" : 'Lao PDR',
                'Republic of Korea' : 'Korea, Rep.',
                'Republic of Moldova' : 'Moldova',
                'Slovakia' : 'Slovak Republic',
                'The former Yugoslav Republic of Macedonia' : 'Macedonia, FYR',
                'United Republic of Tanzania' :  'Tanzania',
                'United States of America' : 'United States',
                'Venezuela (Bolivarian Republic of)' : 'Venezuela, RB',
                'Viet Nam' : 'Vietnam',
                'Yemen' : 'Yemen, Rep.',
                'Antigua & Barbuda' : 'Antigua and Barbuda',
                'Bosnia' : 'Bosnia and Herzegovina',
                'Dominican Rep' : 'Dominican Republic',
                'Iran' : 'Iran, Islamic Rep.',
                'Korea North' : 'Korea, Dem. People’s Rep.',
                'Korea South' : 'Korea, Rep.',
                'Laos' : 'Lao PDR',
                'Macedonia' : 'Macedonia, FYR',
                'Russia' : 'Russian Federation',
                'Syria' : 'Syrian Arab Republic',
                'Trinidad' : 'Trinidad and Tobago',
                'UAE' : 'United Arab Emirates',
                'Venezuela' : 'Venezuela, RB',
                'Bahamas' :  'Bahamas, The',
                'Cape Verde' :  'Cabo Verde',
                'East Timor' : 'Timor-Leste',
                'Micronesia, Fed Stat' : 'Micronesia, Fed. Sts.',
                'Sao Tome' : 'Sao Tome and Principe',
                'St. Kitts & Nevis' : 'St. Kitts and Nevis',
                'St. Vincent & Grenadine' : 'St. Vincent and the Grenadines',
                'Micronesia (Federated States of)' : 'Micronesia, Fed. Sts.',
                'Saint Kitts and Nevis' : 'St. Kitts and Nevis',
                'Saint Vincent and the Grenadines' : 'St. Vincent and the Grenadines',
                'United States Virgin Islands' : 'Virgin Islands (U.S.)',
                'Saint Lucia' : 'St. Lucia'
                 }

for k, v in replace_names.items():
    df.rename(columns={k: v}, inplace=True)

for name in exclude_countries:
    try:
        del df[name]
    except KeyError:
        print("Column %s not in this dataframe" % name)

# To normalize by world average for that year we need to perform few other steps -
# ... load the population data

pop = pd.read_csv('../processed/population_estimates_and_projections.csv')

#replace some of the country names with the ones used in world bank dataset
for k,v in replace_names.items():
    pop.rename(columns = { k : v}, inplace = True)

#get rid of the countries we don't want
for name in exclude_countries:
    try:
        del pop[name]
    except KeyError:
        #print("Column %s not in this dataframe" % name)
        continue

# add world column to democracy data
df['World'] = np.nan
# calculate world averages for all years
for i in range(1960, 2013):
    pop_row = population.loc[i]
    dem_row = df.loc[i]

    total_pop = np.sum(pop_row[df.columns])

    sum_dem_pop = 0

    for country in dem_row.index:
        try:
            pop = pop_row[country]  # get population for country
            dem = dem_row[country]  # get democracy index for country
        except KeyError: #in case one of the data frames doesn't have a country by that name...
            continue

        weighted_dem = pop * dem
        if not np.isnan(weighted_dem):
            sum_dem_pop += weighted_dem

    world_dem = sum_dem_pop / total_pop
    df.loc[i]['World'] = world_dem

#shift all values up by 5 to get rid of negatives
df = df.add(5)

df.to_csv('../processed/democracy_scores.csv')

# normalize by world averages:
df_norm = df.loc[:, df.columns != 'World'].div(df['World'].values, axis=0) #divide all values by the world values

df_norm.to_csv('../processed/democracy_scores_normalized.csv')