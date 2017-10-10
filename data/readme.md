# List of data sources and files used

Please always add the source you used to this file for any data you download

## GDP per capita (current US$)

* Source: https://data.worldbank.org/indicator/NY.GDP.PCAP.CD
* Raw: API_NY.GDP.PCAP.CD_DS2_en_csv_v2/API_NY.GDP.PCAP.CD_DS2_en_csv_v2.csv
* Processed: 
  * gdp_per_capita_current_usd.csv
  * gdp_per_capita_current_usd_normalized.csv

## Different crops

* Source: http://www.fao.org/faostat/en/#data/QC
* Raw: Production_Crops_E_All_Data.zip and Production_Crops_E_All_Data_(Normalized).zip
* Processed:
  * Format is 'item-element.csv' where item is e.g. 'Almonds, with shell' or 'Wheat'
    and element is e.g. 'area_harvested' or 'seed'
  * Normalized follow same syntax except they add '_normalized' before file extension

