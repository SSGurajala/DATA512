# DATA 512 Common Analysis
## Author : Saisriram Gurajala
## Contact sgura99@uw.edu with any questions and issues

## Goal

The goal of this project is to explore the relationship between wildfire smoke and air quality index in Dearborn Michigan, as the first step of DATA512's final project.

## Repository Structure 

This github has the following structure, generated through the tree command in linux. 

```
data-512-common-analysis
├── LICENSE
├── README.md
├── data
│   ├── AQI_Dearborn_Michigan.csv
│   ├── USGS_Wildland_Fire_Combined_Dataset.json
│   ├── USGS_Wildland_Fire_Combined_Dataset_filtered.json
├── imgs
│   ├── acreage_burned_line_plot.png
│   ├── aqi_smoke_metric_line_plot.png
│   ├── histogram_plot.png
│   └── smoke_metric_line_plot_forecast.png
├── logs
│   ├── api_call.log
│   └── geojson_loading.log
└── src
    ├── libs
    │   ├── Reader.py
    │   ├── api_call_AQI.py
    │   ├── api_key_store.py
    │   ├── helpers.py
    │   └── load_and_filter_json.py
    └── notebooks
        ├── data_analysis.ipynb
        ├── data_loading.ipynb
        ├── epa_air_quality_history_example.ipynb
        └── wildfire_geo_proximity_example.ipynb
```

## Data Source, Documentation, and Licensure 

The source data comes from the US geological survey's (USGS) [Combined Wildland Fire Datasets for the US and territories 1800-Present](https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81).  

Additionally, the AQI data comes from US Environmental Protection Agency (EPA) Air Quality Service (AQS) API. Documentation for this API can be found [here](https://aqs.epa.gov/aqsweb/documents/data_api.html). 

Portions of the source code were sourced from notebooks and code created by Dr. David W. McDonald for use in DATA 512 licensed via the [Creative Commons BY](https://creativecommons.org/licenses/by/4.0/). The original, unaltered notebook code is located in the `src/notebooks` directory. 


## Data Files and Outputs

The initial dataset file is found from the USGS survey data: `USGS_Wildland_Fire_Combined_Dataset.json`. However, this file is too large to be provided via GitHub and has thus been placed in a .gitignore file for this directory. However, we note that the original file is in geojson format. The official schema for the geojson file type can be found [here](https://geojson.org/schema/GeoJSON.json). 

This data wrangling and analysis pipeline also produces a final output required for the visualizations: `USGS_Wildland_Fire_Combined_Dataset_filtered.json`. However, this file is also too large to upload to github and has been placed in the .gitignore. This record is simply the subfields of the attributes field of the original geojson file, and also includes a subfield for the distance to Dearborn, MI. A sample record from this file is shown below: 

```
{'OBJECTID': 13533,
 'USGS_Assigned_ID': 13533,
 'Assigned_Fire_Type': 'Wildfire',
 'Fire_Year': 1961,
 'Fire_Polygon_Tier': 1,
 'Fire_Attribute_Tiers': '1 (1), 3 (3)',
 'GIS_Acres': 13511.581888853605,
 'GIS_Hectares': 5467.943194369074,
 'Source_Datasets': 'Comb_National_NIFC_Interagency_Fire_Perimeter_History (1), Comb_National_WFDSS_Interagency_Fire_Perimeter_History (1), Comb_National_USFS_Northern_Rockies_1889_2003 (1), Comb_National_USFS_Final_Fire_Perimeter (1)',
 'Listed_Fire_Types': 'Wildfire (2), Likely Wildfire (2)',
 'Listed_Fire_Names': 'Corn Creek (2), SLEEPING CHILD (1), No Fire Name Provided (1)',
 'Listed_Fire_Codes': 'No code provided (4)',
 'Listed_Fire_IDs': '',
 'Listed_Fire_IRWIN_IDs': '',
 'Listed_Fire_Dates': 'Listed Wildfire Discovery Date(s): 1961-07-24 (1) | Listed Other Fire Date(s): 1899-12-30 - REVDATE field (1)',
 'Listed_Fire_Causes': '',
 'Listed_Fire_Cause_Class': 'Undetermined (4)',
 'Listed_Rx_Reported_Acres': None,
 'Listed_Map_Digitize_Methods': 'Digitized Other (1)',
 'Listed_Notes': '1 death heart attack, 1 died in vehicle accident off forest (2)',
 'Processing_Notes': '',
 'Wildfire_Notice': 'Wildfire mapping prior to 1984 was inconsistent, infrequent, and done without the aid of more modern fire mapping methods (GPS and satellite imagery). Areas burned prior to 1984 in this dataset represent only a fraction of what actually burned. While areas burned on or after 1984 are much more accurate and complete, errors still can and do occur. This dataset represents the most complete set of digitized polygon fire data available to the public that we, the authors, were able to collect. It is not a complete collection of all wildfires burned during the time period it represents.',
 'Prescribed_Burn_Notice': 'Prescribed fire data in this dataset represents only a fraction of the area burned in prescribed burns across all years due to lack of reporting, particularly on private lands. The missing prescribed burn data becomes more pronounced further back in time, particularly in the southeastern U.S.; however, errors and omissions still occur through the most recent years in this dataset. This dataset represents the most complete set of digitized polygon fire data available to the public that we, the authors, were able to collect. It is not a complete collection of all prescribed burns burned during the time period it represents.',
 'Wildfire_and_Rx_Flag': None,
 'Overlap_Within_1_or_2_Flag': None,
 'Circleness_Scale': 0.4089354302200108,
 'Circle_Flag': None,
 'Exclude_From_Summary_Rasters': 'No',
 'Shape_Length': 40991.098725516786,
 'Shape_Area': 54679431.94369074,
 'Distance_to_DearbornMI': 1572.827171297372}
```

Another final output from this script is the included `data/AQI_Dearborn_Michigan.csv` file containing the output of the API Calls. This file contains the date, the maximum average AQI for a given parameter for that date, and the year corresponding to the date. The head output of this csv is as follows:
```
date,aqi,year
2021-05-01,42.5,2021
2021-05-02,54.5,2021
2021-05-03,45.0,2021
2021-05-04,44.294117647058826,2021
2021-05-05,36.0,2021
2021-05-06,42.5,2021
2021-05-07,42.8125,2021
2021-05-08,32.0,2021
2021-05-09,33.5,2021
```