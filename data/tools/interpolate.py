# The code below handles interpolating the values in the data processed data files
# The idea is to create as much coverage as possible for our training data
import pandas as pd
import numpy as np

harmonized_files = [
    'age_dependency_ratio_normalized_nh.csv',
    'ages_65_and_older_percentage_normalized_nh.csv',
    'agricultproductstotal-export_value_base_price_normalized_nh.csv',
    'agricultproductstotal-import_value_base_period_price_normalized_nh.csv',
    'annual_co_emissions_per_country_normalized_nh.csv',
    'births_per_1000_normalized_nh.csv',
    'co_emissions_per_capita_international_normalized_nh.csv',
    'daily_per_capita_fat_supply_normalized_nh.csv',
    'daily_per_capita_protein_supply_normalized_nh.csv',
    'daily_per_capita_supply_of_calories_normalized_nh.csv',
    'deaths_per_1000_normalized_nh.csv',
    'democracy_scores_normalized_nh.csv',
    'exports_of_goods_and_services_percentage_of_gdp_normalized_nh.csv',
    'fertility_rate_normalized_nh.csv',
    'food_excl_fish-export_value_base_price_normalized_nh.csv',
    'food_excl_fish-import_value_base_period_price_normalized_nh.csv',
    'gdp_per_capita_current_usd_nh.csv',
    'gross_capital_formation_normalized_nh.csv',
    'historical_gov_spending_gdp_normalized_nh.csv',
    'imports_of_goods_and_services_percentage_of_gdp_normalized_nh.csv',
    'infant_mortality_per_1000_normalized_nh.csv',
    'life_expectancy_female_normalized_nh.csv',
    'life_expectancy_male_normalized_nh.csv',
    'life_expectancy_normalized_nh.csv',
    'military_expenditure_as_share_of_gdp_normalized_nh.csv',
     #'net_migration_nh.csv',
    'population_estimates_and_projections_normalized_nh.csv',
    'pupil-teacher_ratio_processed_nh.csv',
    'rural_population_percentage_normalized_nh.csv',
    'share_of_a_countrys_population_that_is_not_born_within_the_country_normalized_nh.csv',
    'surface_area_sq_km_nh.csv',
    'trade_as_share_of_gdp_normalized_nh.csv',
    'young_pregnancies_normalized_nh.csv'
]

processed_path = './data/processed/'

# load the needed features into a collection of data frames
feature_data = {}
nan_ratios = {}

#############
# Step 1: Load files and generate stats
#############

# generate nan statistics so we know which file to start with :)
for filename in harmonized_files :
    df = pd.read_csv(processed_path + filename, index_col=0)
    # drop data that is too old
    df = df.drop(df.index[df.index < 1960])
    # Which years are we missing?
    needed_years = list(range(1960,2016))
    missing_values = set(needed_years) - set(df.index.values)
    # add new rows for the missing years (some CSVs have data until 2012, we want to pad them until 2015)
    df.reindex(df.index.union(missing_values))
    feature_data[filename] = df

    # count nans per column statistics
    nanratio = 0
    for c in df.columns.values:
        try:
            nanratio += df[c].value_counts(dropna=False)[np.nan]/len(df[c])
        except KeyError:
            continue

    nan_ratios[filename] = {}
    nan_ratios[filename]['before'] = nanratio/len(df.columns)

#print out a sorted list of statitics of the proportion of NaNs in each data frame of interest
print("Nan ratios before:")
for k in sorted(nan_ratios, key=lambda x: (nan_ratios[x]['before']), reverse=True):
    print("File %s has %f NaNs" %(k, nan_ratios[k]['before']))


#############
# Step 2: Interpolate and show updated stats
#############

# Interpolate series
# s series
# lim how many consecutive values to fill
# method algorithm to use
# dir direction of interpolation
# the above are specified for 2 passes (1 first path, 2 second pass)
def interpolate_s(s, lim1, lim2, method1, method2, dir1, dir2):
    try:
        # first pass - use a more advanced method
        s = s.interpolate(method1, limit_direction=dir1, limit=lim1)
        # second pass - fill the gaps with linear method
        s = s.interpolate(method2, limit_direction=dir2, limit=lim2)
    except (ValueError, UnboundLocalError) as e:
        print("Value error with: ", s.name)
    return s


# Interpolate the entire data frame
# df data frame to interpolate
# the rest of parameters same as above
def interpolate_df(df, lim1, lim2, method1, method2, dir1, dir2):
    for col in df.columns.values:
        df[col] = interpolate_s(df[col], lim1, lim2, method1, method2, dir1, dir2)
    return df


# Good parameters found by experiment
# Pass 1: Akima, 4 steps, both directions
# Pass 2: Linear, 2 steps, both directions (linear has a negative feature of drawing a horizontal line
# when doing backwards interpolation :(

# Interpolate!

interpolated_data = {}

for filename in harmonized_files:
    interpolated_data[filename] = interpolate_df(feature_data[filename], 6, 5, 'akima', 'linear', 'both', 'forward')
    interpolated_csv_name = filename.split('.')[0] + '_ip.csv'
    interpolated_data[filename].to_csv('data/processed/interpolated/' + interpolated_csv_name )

# generate stats after
for filename in harmonized_files :
    df = interpolated_data[filename]

    # count nans per column statistics
    nanratio = 0
    for c in df.columns.values:
        try:
            nanratio += df[c].value_counts(dropna=False)[np.nan]/len(df[c])
        except KeyError:
            continue

    nan_ratios[filename] = {}
    nan_ratios[filename]['after'] = nanratio/len(df.columns)

#print out a sorted list of statitics of the proportion of NaNs in each data frame of interest
print("Nan ratios after:")
for k in sorted(nan_ratios, key=lambda x: (nan_ratios[x]['after']), reverse=True):
    print("File %s has %f NaNs" %(k, nan_ratios[k]['after']))