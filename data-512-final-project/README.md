# DATA 512 Final Project
## Author : Saisriram Gurajala
## Contact sgura99@uw.edu with any questions and issues

## Goal 

The goal of this project is to understand the link between wildfire smoke and chronic respiratory disease incidence in Dearborn Michigan. 

## Repository Structure

The following is the output of the tree command on this repo:

```
data-512-final-project
├── LICENSE
├── README.md
├── data
│   ├── final
│   │   ├── AQI_Dearborn_Michigan.csv
│   │   ├── USGS_wildfire_dearborn_filtered.csv
│   │   ├── gbd_aggregated_death_metric_per_year.csv
│   │   ├── gbd_aggregated_incidence_metric_per_year.csv
│   │   └── ncei_cleaned_final.csv
│   └── raw
│       ├── AQI_Dearborn_Michigan.csv
│       ├── IHME-GBD_2021_DATA-5c7069d7-1.csv
│       ├── NCEI_drought_severity_index_data_raw.csv
│       ├── NCEI_precipitation_data_raw.csv
│       ├── NCEI_temperature_data_raw.csv
│       └── USGS_Wildland_Fire_Combined_Dataset_filtered.json
├── img
│   └── forecast_smoke.png
└── src
    └── notebooks
        ├── data_analysis.ipynb
        ├── data_wrangling_gbd.ipynb
        ├── data_wrangling_ncei.ipynb
        └── data_wrangling_usgs.ipynb
```

## Data Sources

This data is sourced from multiple sources:

- The wildfire data is sourced from the US geological survey's (USGS) [Combined Wildland Fire Datasets for the US and territories 1800-Present](https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81). 
- The climate and precipitation data is sourced from the National Oceanic and Atmospheric Administration's (NOAA) National Center for Environmental Information (NCEI) [Climate at a Glance](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/) web-service.
- The chronic respiratory disease data is sourced from the Institute for Health Metrics and Evaluation's [Global Disease Burden Study](https://www.healthdata.org/research-analysis/gbd).
- The air quality data is sourced from the US Environmental Protection Agency (EPA) Air Quality Service (AQS) API. Documentation for this API can be found [here](https://aqs.epa.gov/aqsweb/documents/data_api.html). 

Parsing and obtaining the wildland fire data and the air quality data was conducted in previous work. The repo housing the code and procedures for this can be found [here](https://github.com/SSGurajala/DATA512/tree/main/data-512-common-analysis). 

## Data Availability 

Two sets of files are unable to be shared in this repo:
- The files from the global burden of disease study are unable to be shared due to licensure agreements.
- The raw files for the USGS wildland fire dataset are too large to house in a github repo. 

## Data Files

Wrangling the data has resulted in the following final data files:

-[USGS_wildfire_dearborn_filtered.csv](data-512-final-project/data/final/USGS_wildfire_dearborn_filtered.csv): The following is the output of the head command on this file. 

|    | FireType   |   Year |   Acreage |   Distance_to_Dearborn |
|---:|:-----------|-------:|----------:|-----------------------:|
|  0 | Wildfire   |   1980 |  1098.9   |                452.855 |
|  1 | Wildfire   |   1980 |   423.179 |                472.746 |
|  2 | Wildfire   |   1980 |   193.681 |                645.901 |
|  3 | Wildfire   |   1980 |   161.465 |                330.567 |
|  4 | Wildfire   |   1980 |   115.361 |                473.31  |


The fields of this dataframe are as follows:

1. FireType: Type: String or Object Description: Indicates the type of fire, and selections include Wildfire or Prescribed Burn. 
2. Year: Type: Integer. Description: The calendar year when the fire occurred.
3. Acreage: Type: Float. Description: Represents the size of the area burned by the wildfire in acres.
4. Distance_to_Dearborn: Type: Float. Description: The distance in miles from the location of the fire to Dearborn, Michigan. 

-[ncei_cleaned_final.csv](data-512-final-project/data/final/ncei_cleaned_final.csv): The following is the output of the head command on this file. 

|    |   Year |   avg_Drought_Severity_Index |   avg_Temperature |   avg_Precipitation |
|---:|-------:|-----------------------------:|------------------:|--------------------:|
|  0 |   1980 |                      2.05167 |           47.2167 |             2.9025  |
|  1 |   1981 |                      2.84583 |           47.8833 |             2.97167 |
|  2 |   1982 |                      2.57833 |           47.8917 |             2.72417 |
|  3 |   1983 |                      2.53083 |           48.8917 |             3.165   |
|  4 |   1984 |                      0.2475  |           48.5    |             2.32083 |

The fields of this dataframe are as follows:

1. Year: Type: Integer. Description: Indicates the calendar year for which the data is recorded.
2. avg_Drought_Severity_Index: Type: Float. Description: Represents the average palmer drought severity index for the year.
3. avg_Temperature: Type: Float. Description: Reflects the average temperature recorded for the year.
4. avg_Precipitation: Type: Float. Description: Indicates the average precipitation  recorded for the year.


-[gbd_aggregated_death_metric_per_year.csv](data-512-final-project/data/final/gbd_aggregated_death_metric_per_year.csv) and [gbd_aggregated_incidence_metric_per_year.csv](data-512-final-project/data/final/gbd_aggregated_incidence_metric_per_year.csv). These files are similarly structured, and are both from the GBD dataset. The following is the output of the head command for the incidence metric per year file. 

|    |   year | measure   |    val |
|---:|-------:|:----------|-------:|
|  0 |   1990 | Incidence | 271367 |
|  1 |   1991 | Incidence | 259067 |
|  2 |   1992 | Incidence | 247234 |
|  3 |   1993 | Incidence | 236616 |
|  4 |   1994 | Incidence | 228423 |

The fields of this dataframe are as follows:

1. year: Type: Integer. Description: Represents the calendar year in which the data point was recorded.
2. measure: Type: String or Object. Description: Describes the type of data being reported. Incidence indicates the number of new cases for a particular condition or event. In this case it describes the number of new chronic respiratory disease cases.
3. val: Type: Integer or numeric. Description: The value associated with the measure, representing the count of new cases (incidence) for the respective year.


-[AQI_Dearborn_Michigan.csv](data-512-final-project/data/final/AQI_Dearborn_Michigan.csv). The following is the output from the head command of the file:

|    | date       |     aqi |   year |
|---:|:-----------|--------:|-------:|
|  0 | 2021-05-01 | 42.5    |   2021 |
|  1 | 2021-05-02 | 54.5    |   2021 |
|  2 | 2021-05-03 | 45      |   2021 |
|  3 | 2021-05-04 | 44.2941 |   2021 |
|  4 | 2021-05-05 | 36      |   2021 |

The fields of this dataframe are as follows: 

1. date: Type: datetime object Description: Represents a specific calendar date in YYYY-MM-DD format.
2. aqi: Type: Float or numeric. Description: Represents the Air Quality Index (AQI) on the corresponding date. AQI measures air quality, with lower values indicating better air quality.
3. year: Type: Integer. Description: Denotes the calendar year in which the observation was recorded (all 2021 in this case).

## Methods 

This project employed statistical modeling methods to craft a smoke metric, forecast the smoke metric, and use it to predict disease incidence.

### Smoke Metric Development

The smoke metric was developed largely empirically by trying different combinations of variables and comparing to air quality index during fire season. The inclusion of climate metrics was prompted by a [study](https://www.publish.csiro.au/WF/WF21145) finding that wildfire smoke correlates with palmer drought severity index in california between 1984 and 2018. The basis of the metric arose from the inverse square law, which forecasts intensity as a function of distance from a central point. I assumed acreage burned is approximates of a fire's intensity, and created a core metric of $$\frac{acreage_{fire}}{{distance}^2_{fire}}$$. I incorporated climate measurements as a multiplier to this metric. Higher average temperature, less precipitation and lower dsi values should make a fire have more impact. Therefore, I crafted a ratio of these three quantities. I adjusted this ratio to better approximate the air quality index, and to this end finalized a squared version of this proportion as the multiplier to the core metric. The metric takes the following form, and was generated for every fire. 

$$SmokeMetric_{fire} = f(acreage_{fire}, distance_{fire}, temperature_{fire}, dsi_{fire}, precipitation_{fire})$$
$$f(acreage_{fire}, distance_{fire}, temperature_{fire}, dsi_{fire}, precipitation_{fire}) = \frac{acreage_{fire}}{{distance}^2_{fire}} * (\frac{temperature_{fire}}{precipitation_{fire} * dsi_{fire}})^2$$



### Smoke Metric Forecasting 

To forecast the smoke metric we used the holt-winters exponential smoothing time series forecasting method. Examining the data, I saw spikes every three to four years in smoke impact so I posited the data was partially periodic. Therefore, I experimented with the seasonal variant of this algorithm. The algorithm itself has been described in many different papers, and I referred to the following articles to guide my work. Briefly, Holt-Winters forecasting is a time series analysis technique that extends exponential smoothing to account for both trends and seasonality in data. It uses three components: level, trend, and seasonality, which are updated with smoothing parameters to produce accurate forecasts. The method comes in two variations—additive and multiplicative—depending on whether the seasonal patterns in the data have a constant magnitude or vary proportionally to the level of the series. Holt-Winters is particularly effective for time series data with regular seasonal fluctuations and trends, providing a robust framework for short- to medium-term forecasting in fields such as finance, inventory management, and demand planning. I implemented the Holt-Winters forecasting method via the statsmodels time series analysis API. 

Holt, C. C. (1957). Forecasting seasonals and trends by exponentially weighted averages (O.N.R. Memorandum No. 52). Carnegie Institute of Technology, Pittsburgh USA. 

Winters, P. R. (1960). Forecasting sales by exponentially weighted moving averages. Management Science, 6(3), 324–342.

Chatfield, C. (1978), "The Holt-Winters Forecasting Procedures," Applied Statistics, 27, 264—279. [1515]

I used the following technical resource for this: [github blog post](https://ostwalprasad.github.io/machine-learning/Polynomial-Regression-using-statsmodel.html). 

Documentation for the statsmodel API is below: 

[statsmodels time series analysis API](https://www.statsmodels.org/stable/api.html)


### Incidence Predictions 

To predict incidence, I opted to use a polynomial regression on the moving average of smoke metric and included a linear term for year using the statsmodel and scikit-learn APIs. Briefly, polynomial regression is a statistical technique that models the relationship between an independent variable and a dependent variable as an nth-degree polynomial. Unlike simple linear regression, which fits a straight line, polynomial regression fits a curved line by introducing powers of the independent variable (e.g., squared, cubed terms) as additional predictors. This allows it to capture non-linear patterns in the data while still being a linear model with respect to its coefficients. It is often used when data exhibits a curvilinear trend that cannot be accurately represented by a straight line, providing more flexibility while maintaining interpretability for lower-degree polynomials. Documentation for these APIs can be found below: 

[sklearn-preprocessing API](https://scikit-learn.org/1.5/api/sklearn.preprocessing.html)

[statsmodels API](https://www.statsmodels.org/stable/api.html)





