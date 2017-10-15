#Usage:
#import replacements
#new_df = replacements.replace_country_names(old_df)

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
                'Virgin Islands, British', 'Liechtenstein', 'Germany East',
                'Kosovo', 'Taiwan', 'Vietnam South',
                'Western Samoa', 'Yemen South']

#country names to replace
replace_names = {'Germany West': 'Germany',
                 'Germany, West' : 'Germany',
                'Congo (Brazzaville)' : 'Congo, Rep.',
                'Congo (Kinshasa)' : 'Congo, Dem. Rep.',
                'Congo Brazzaville' : 'Congo, Rep.',
                'Congo Kinshasa': 'Congo, Dem. Rep.',
                'Burma (Myanmar)' : 'Myanmar',
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
                'Korea, North' : 'Korea, Dem. People’s Rep.',
                'Korea, South' : 'Korea, Rep.',
                'Korea North' : 'Korea, Dem. People’s Rep.',
                'Korea South' : 'Korea, Rep.',
                'Laos' : 'Lao PDR',
                'Macedonia' : 'Macedonia, FYR',
                'Russia' : 'Russian Federation',
                'Syria' : 'Syrian Arab Republic',
                'Trinidad' : 'Trinidad and Tobago',
                'UAE' : 'United Arab Emirates',
                'Venezuela' : 'Venezuela, RB',
                'Bahamas' : 'Bahamas, The',
                'Cape Verde' : 'Cabo Verde',
                'East Timor' : 'Timor-Leste',
                'Micronesia, Fed Stat' : 'Micronesia, Fed. Sts.',
                'Sao Tome' : 'Sao Tome and Principe',
                'St. Kitts & Nevis' : 'St. Kitts and Nevis',
                'St. Vincent & Grenadine' : 'St. Vincent and the Grenadines',
                'Micronesia (Federated States of)' : 'Micronesia, Fed. Sts.',
                'Saint Kitts and Nevis' : 'St. Kitts and Nevis',
                'Saint Vincent and the Grenadines' : 'St. Vincent and the Grenadines',
                'United States Virgin Islands' : 'Virgin Islands (U.S.)',
                'Saint Lucia' : 'St. Lucia',
                'Micronesia' : 'Micronesia, Fed. Sts.',
                'American Samoa' : 'Samoa',
                'Brunei' :  'Brunei Darussalam',
                'Cote dIvoire (IvoryCoast)' :  "Cote d'Ivoire",
                'Hong Kong': 'Hong Kong SAR, China',
                'Macau' : 'Macao SAR, China',
                'Palestinian Territories' : 'West Bank and Gaza',
                'Saint Vincent/Grenadines' : 'St. Vincent and the Grenadines',
                'Timor-Leste (East Timor)' : 'Timor-Leste',
                'Virgin Islands,  U.S.' :  'Virgin Islands (U.S.)',
                'Democratic Republic of Congo': 'Congo, Dem. Rep.',
                'Macao': 'Macao SAR, China',
                'Micronesia (country)': 'Micronesia, Fed. Sts.',
                'North Korea': 'Korea, Dem. People’s Rep.',
                'South Korea': 'Korea, Rep.',
                'Timor': 'Timor-Leste',
                'Bosnia/Herzegovina': 'Bosnia and Herzegovina',
                'Central African Rep.': 'Central African Republic',
                'China, Hong Kong': 'Hong Kong SAR, China',
                'China, Macao': 'Macao SAR, China',
                'Curaçao': 'Curacao',
                'Korea, DPR': 'Korea, Dem. People’s Rep.',
                'Saint-Martin': 'St. Martin (French part)',
                'Sint Maarten': 'Sint Maarten (Dutch part)',
                'St Vincent/Grenadines': 'St. Vincent and the Grenadines',
                'TFYR Macedonia': 'Macedonia, FYR',
                'Virgin Islands, USA': 'Virgin Islands (U.S.)'
                 }

def replace_country_names(df, verbose=False):
    _df = df.copy()

    #replace country names to be the same across all data sets
    for k, v in replace_names.items():
        _df.rename(columns={k: v}, inplace=True)

    #remove countries we don't want to analyze
    for name in exclude_countries:
        try:
            del _df[name]
        except KeyError:
            if verbose :
                print("Column %s not in this dataframe" % name)
            continue
    return _df