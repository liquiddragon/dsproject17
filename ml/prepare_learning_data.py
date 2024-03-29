'''
Reads in processed data from the ../data/processed folder and creates a list of feature
vectors of the following form:

[country+year, feature1, feature2, feature3, ... , feature n, label Y or regression value Y]

For each year, the label/regression value correspond to the value in the year 15 years
after the data point.
'''

import pandas as pd
import sys
import os


raw_features = [
    # [feature/file name, add to learning data (yes/no), number of lags (how many previous years to include)]
    ['age_dependency_ratio', False, 1],
    ['age_dependency_ratio_normalized', True, 3],
    ['ages_65_and_older_percentage', False, 1],
    ['ages_65_and_older_percentage_normalized', True, 1],
    ['agricultproductstotal-export_value_base_price', False, 1],
    ['agricultproductstotal-export_value_base_price_normalized', True, 3],
    ['agricultproductstotal-import_value_base_period_price', False, 1],
    ['agricultproductstotal-import_value_base_period_price_normalized', True, 3],
    ['annual_co_emissions_per_country', False, 1],
    ['annual_co_emissions_per_country_normalized', True, 3],
    ['births_per_1000', False, 1],
    ['births_per_1000_normalized', True, 3],
    ['co_emissions_per_capita_international', False, 1],
    ['co_emissions_per_capita_international_normalized', True, 3],
    ['daily_per_capita_fat_supply', False, 1],
    ['daily_per_capita_fat_supply_normalized', True, 3],
    ['daily_per_capita_protein_supply', False, 1],
    ['daily_per_capita_protein_supply_normalized', True, 3],
    ['daily_per_capita_supply_of_calories', False, 1],
    ['daily_per_capita_supply_of_calories_normalized', True, 3],
    ['deaths_per_1000', False, 1],
    ['deaths_per_1000_normalized', True, 1],
    ['democracy_scores', False, 1],
    ['democracy_scores_normalized', True, 3],
    ['exports_of_goods_and_services_percentage_of_gdp', False, 1],
    ['exports_of_goods_and_services_percentage_of_gdp_normalized', True, 3],
    ['fertility_rate', False, 1],
    ['fertility_rate_normalized', True, 3],
    ['food_excl_fish-export_value_base_price', False, 1],
    ['food_excl_fish-export_value_base_price_normalized', True, 3],
    ['food_excl_fish-import_value_base_period_price', False, 1],
    ['food_excl_fish-import_value_base_period_price_normalized', True, 3],
    ['gross_capital_formation', False, 1],
    ['gross_capital_formation_normalized', True, 3],
    ['historical_gov_spending_gdp', False, 1],
    ['historical_gov_spending_gdp_normalized', True, 3],
    ['imports_of_goods_and_services_percentage_of_gdp', False, 1],
    ['imports_of_goods_and_services_percentage_of_gdp_normalized', True, 3],
    ['infant_mortality_per_1000', False, 1],
    ['infant_mortality_per_1000_normalized', True, 3],
    ['life_expectancy', False, 1],
    ['life_expectancy_female', False, 1],
    ['life_expectancy_female_normalized', True, 3],
    ['life_expectancy_male', False, 1],
    ['life_expectancy_male_normalized', True, 3],
    ['life_expectancy_normalized', True, 3],
    ['mean_years_of_schooling_selected_countries', False, 1],
    ['mean_years_of_schooling_selected_countries_normalized', False, 1],
    ['military_expenditure_as_share_of_gdp', False, 1],
    ['military_expenditure_as_share_of_gdp_normalized', True, 3],
    #['net_migration', True, 1], Need to normalize!
    ['population_estimates_and_projections', False, 1],
    ['population_estimates_and_projections_normalized', True, 3],
    ['primary_enrollment_selected_countries', False, 1],
    ['primary_enrollment_selected_countries_normalized', False, 1],
    ['pupil-teacher_ratio_processed', True, 3],
    ['rural_population_percentage', False, 1],
    ['rural_population_percentage_normalized', True, 3],
    ['share_of_a_countrys_population_that_is_not_born_within_the_country', False, 1],
    ['share_of_a_countrys_population_that_is_not_born_within_the_country_normalized', True, 3],
    ['surface_area_sq_km', True, 1],
    ['trade_as_share_of_gdp', False, 1],
    ['trade_as_share_of_gdp_normalized', True, 3],
    ['young_pregnancies', False, 1],
    ['young_pregnancies_normalized', True, 3]
]

raw_labels = 'gdp_per_capita_current_usd_nh_ip.csv'
# ['gdp_per_capita_current_usd.csv', False, 1],
# ['gdp_per_capita_current_usd_normalized.csv', True, 1],

processed_path = 'data/processed/interpolated/'

feature_columns = [entry[0] for entry in raw_features if entry[1]]

# load the needed features into a collection of data frames
feature_data = {}
# store lag data per country
lag_data = {key: value for (key, value) in [(entry[0], entry[2]) for entry in raw_features if entry[1]]}


for c in feature_columns :
    feature_data[c] = pd.read_csv(processed_path + c +'_nh_ip.csv', index_col=0)

label_data = pd.read_csv(processed_path + raw_labels, index_col=0)



# spot check that columns are reasonable
# for i in feature_data :
#    print('Name %s, value %s '%(i, feature_data[i].columns[5]))

#get a list of countries that are shared by all data frames:
country_sets = []

for f in feature_data :
    country_sets.append(set(feature_data[f].columns))

country_names_set = set.intersection(*country_sets)

# create new dataframe that will contain features and labels for training
years = list(range(1961, 2001))
#for the first try we just go with the list of names in the label data.
countries = label_data.columns #use world bank country list for now
indices = [ country + ' : ' + str(year) for country in countries for year in years  ]

columns = feature_columns + ['gdp_in_15_years']

df_for_ml = pd.DataFrame(index=indices, columns=columns)

#populate data frame:
for i in df_for_ml.index.values:
    country, year = i.split(' : ')
    year = int(year)
    #populate feature columns
    for c in df_for_ml.columns.values:
        try:
            df_for_ml.loc[i][c] = feature_data[c].loc[year][country]
        except (KeyError, IndexError) as e:
            continue
    #populate label column (GDP data 15 years later)
    try :
        df_for_ml.loc[i]['gdp_in_15_years'] = label_data.loc[year + 15][country] / label_data.loc[int(year)][country]
    except (KeyError, IndexError) as e:
        continue

#save data to CSV
df_for_ml.to_csv('ml/training/data_interpolated.csv')

##############################################
# Create another dataframe for recent years:
##############################################

years2 = list(range(2001, 2016))
# for the first try we just go with the list of names in the label data.
countries = label_data.columns #use world bank country list for now
indices2 = [country + ' : ' + str(year) for country in countries for year in years2]

columns2 = feature_columns + ['gdp_per_capita']

df_recent = pd.DataFrame(index=indices2, columns=columns2)

# populate data frame:
for i in df_recent.index.values:
    country, year = i.split(' : ')
    year = int(year)
    # populate feature columns
    for c in df_recent.columns.values:
        try:
            df_recent.loc[i][c] = feature_data[c].loc[year][country]
        except (KeyError, IndexError) as e:
            continue
    # populate label column with current GDP
    try:
        df_recent.loc[i]['gdp_per_capita'] = label_data.loc[int(year)][country]
    except (KeyError, IndexError) as e:
        continue

# save data to CSV
df_recent.to_csv('ml/training/data_up_till_now_interpolated.csv')