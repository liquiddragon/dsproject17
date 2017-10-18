# Tools used

Here are tools used to obtain processed outputs, if necessary.

## FAO crops
Use these two scripts in same directory where you have CSV files from Production_Crops_E_All_Data.zip and Production_Crops_E_All_Data_(Normalized).zip extacted. They will produce one file per item and per element such as 'wheat-seed.csv'. Both scripts use Python 3 and expect to have Pandas available.
* production_crops_all_process.py
* production_crops_normalized_all_process.py

## FAO trade indices
This script reads raw data and produces two output files containing parsed and normalized datasets.
* trade_indices_all_process.py

## FAO population
This script reads raw data and produces two output files containing parsed and normalized datasets.
* population_all_process.py

## Out world in data
This script reads different raw data and produces two output files containing parsed and normalized datasets.
* our_world_in_data_process.py

It expects following command line parameters: "input file name" "country name index" "year index" "value index" "-p as optional parameter for percentage values" "output file name"

## World Bank
This scripts reads all World Bank data from the specified directories and outputs processed CSVs.
* world_bank_all_process.py

## Democracy Scores
Reads and normalizes Democracy scores, by using population data from FAO
* unified_democracy_scores_process.py

## Country name replacement script
Replaces country names in data frame columns to match those used by World Bank data set.  
Usage:  

import replacements  
new_df = replacements.replace_country_names(old_df)  

* replacements.py

## Name harmonizer
Use this to harmonize column names on CSV files. You will need Python library called 'fuzzywuzzy' with preferably its speedup version. In addition list of country names, such as included countries.csv here, is required. You may modify file inclusion and exclusion lists by modifying script code itself.
* name_harmonizer.py
* countries.csv

