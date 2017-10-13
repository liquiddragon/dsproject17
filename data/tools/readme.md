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
