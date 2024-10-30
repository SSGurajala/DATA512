import requests
import json
import time 
from api_key_store import Api_Key_Store
import os
import logging
import datetime
import pandas as pd
os.chdir(os.getenv("DATA512_BASE_FILE_PATH"))

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=f"./logs/api_call.log")

OUT_FILE = "data/AQI_Dearborn_Michigan.csv"

#########
#
#    CONSTANTS
#

#   API Key store to not expose api key endpoint
api_key_store = Api_Key_Store()

#
#    This is the root of all AQS API URLs
#
API_REQUEST_URL = 'https://aqs.epa.gov/data/api'

#
#    These are some of the 'actions' we can ask the API to take or requests that we can make of the API
#
#    Sign-up request - generally only performed once - unless you lose your key
API_ACTION_SIGNUP = '/signup?email={email}'
#
#    List actions provide information on API parameter values that are required by some other actions/requests
API_ACTION_LIST_CLASSES = '/list/classes?email={email}&key={key}'
API_ACTION_LIST_PARAMS = '/list/parametersByClass?email={email}&key={key}&pc={pclass}'
API_ACTION_LIST_SITES = '/list/sitesByCounty?email={email}&key={key}&state={state}&county={county}'
#
#    Monitor actions are requests for monitoring stations that meet specific criteria
API_ACTION_MONITORS_COUNTY = '/monitors/byCounty?email={email}&key={key}&param={param}&bdate={begin_date}&edate={end_date}&state={state}&county={county}'
API_ACTION_MONITORS_BOX = '/monitors/byBox?email={email}&key={key}&param={param}&bdate={begin_date}&edate={end_date}&minlat={minlat}&maxlat={maxlat}&minlon={minlon}&maxlon={maxlon}'
#
#    Summary actions are requests for summary data. These are for daily summaries
API_ACTION_DAILY_SUMMARY_COUNTY = '/dailyData/byCounty?email={email}&key={key}&param={param}&bdate={begin_date}&edate={end_date}&state={state}&county={county}'
API_ACTION_DAILY_SUMMARY_BOX = '/dailyData/byBox?email={email}&key={key}&param={param}&bdate={begin_date}&edate={end_date}&minlat={minlat}&maxlat={maxlat}&minlon={minlon}&maxlon={maxlon}'
#
#    It is always nice to be respectful of a free data resource.
#    We're going to observe a 100 requests per minute limit - which is fairly nice
API_LATENCY_ASSUMED = 0.002       # Assuming roughly 2ms latency on the API and network
API_THROTTLE_WAIT = (1.0/100.0)-API_LATENCY_ASSUMED
#
#
#    This is a template that covers most of the parameters for the actions we might take, from the set of actions
#    above. In the examples below, most of the time parameters can either be supplied as individual values to a
#    function - or they can be set in a copy of the template and passed in with the template.
# 
AQS_REQUEST_TEMPLATE = {
    "email":      "",     
    "key":        "",      
    "state":      "26",     # the two digit state FIPS # as a string
    "county":     "163",     # the three digit county FIPS # as a string
    "begin_date": "",     # the start of a time window in YYYYMMDD format
    "end_date":   "",     # the end of a time window in YYYYMMDD format, begin_date and end_date must be in the same year
    "minlat":    0.0,
    "maxlat":    0.0,
    "minlon":    0.0,
    "maxlon":    0.0,
    "param":     "",     # a list of comma separated 5 digit codes, max 5 codes requested
    "pclass":    ""      # parameter class is only used by the List calls
}

AQI_PARAMS_GASEOUS = "42101,42401,42602,44201"
#
#   Particulate AQI pollutants PM10, PM2.5, and Acceptable PM2.5
AQI_PARAMS_PARTICULATES = "81102,88101,88502"

def request_daily_summary(param=None,
                           begin_date=None, 
                           end_date=None, 
                           fips=None,
                           endpoint_url = API_REQUEST_URL, 
                           api_key_store=api_key_store,
                           endpoint_action = API_ACTION_DAILY_SUMMARY_COUNTY, 
                           request_template = AQS_REQUEST_TEMPLATE,
                           headers = None):
    
    #  This prioritizes the info from the call parameters - not what's already in the template
    if api_key_store:
        request_template['email'] = api_key_store.username
        request_template['key'] = api_key_store.key
    if param:
        request_template['param'] = param
    if begin_date:
        request_template['begin_date'] = begin_date
    if end_date:
        request_template['end_date'] = end_date
    if fips and len(fips)==5:
        request_template['state'] = fips[:2]
        request_template['county'] = fips[2:]            

    # Make sure there are values that allow us to make a call - these are always required
    if not request_template['email']:
        raise Exception("Must supply an email address to call 'request_daily_summary()'")
    if not request_template['key']: 
        raise Exception("Must supply a key to call 'request_daily_summary()'")
    if not request_template['param']: 
        raise Exception("Must supply param values to call 'request_daily_summary()'")
    if not request_template['begin_date']: 
        raise Exception("Must supply a begin_date to call 'request_daily_summary()'")
    if not request_template['end_date']: 
        raise Exception("Must supply an end_date to call 'request_daily_summary()'")
    # Note we're not validating FIPS fields because not all of the annual summary actions require the FIPS numbers
    # compose the request
    request_url = endpoint_url+endpoint_action.format(**request_template)
    # make the request
    try:
        # Wait first, to make sure we don't exceed a rate limit in the situation where an exception occurs
        # during the request processing - throttling is always a good practice with a free data source
        if API_THROTTLE_WAIT > 0.0:
            time.sleep(API_THROTTLE_WAIT)
        response = requests.get(request_url, headers=headers)
        json_response = response.json()
        logging.info(f"API Pull for {begin_date} to {end_date} succeeded for param {param}.")
    except Exception as e:
        logging.info(f"API Pull for {begin_date} to {end_date} for param {param} failed due to reason {e}.")
        json_response = None
    
    if json_response['Data'] == []:
        logging.info(f"No data available for API Call of {begin_date} to {end_date} for param {param}.")
        json_response = None
    return json_response

def consolidate_results(res_gas = None, 
                        res_particulates = None,
                        year = None):
    if not res_gas and not res_particulates:
        logging.info("Must provide valid data to consolidate!")
        response_df = None
        return response_df 
    if not year:
        logging.info("Must provide a valid year to consolidate data")
        response_df = None
        return response_df
    #set upper and lower bounds for years
    lower_bound = datetime.datetime.strptime(f"{year}-05-01", "%Y-%m-%d")
    upper_bound = datetime.datetime.strptime(f"{year}-10-31", "%Y-%m-%d")
    response_dataframes = []
    #consolidate res for gas
    try:
        if res_gas: 
            for response in res_gas['Data']:
                res_date = datetime.datetime.strptime(response['date_local'], "%Y-%m-%d")
                if res_date >= lower_bound and res_date <= upper_bound:
                    res_df = pd.DataFrame({"date" : [response['date_local']],
                                        "parameter" : [response['parameter']],
                                        "aqi" : [response['aqi']]})
                    response_dataframes.append(res_df)
        #consolidate res for particulates
        if res_particulates:
            for response in res_particulates['Data']:
                res_date = datetime.datetime.strptime(response['date_local'], "%Y-%m-%d")
                if res_date >= lower_bound and res_date <= upper_bound:
                    res_df = pd.DataFrame({"date" : [response['date_local']],
                                        "parameter" : [response['parameter']],
                                        "aqi" : [response['aqi']]})
                    response_dataframes.append(res_df)
        #take mean per date and parameter
        response_df = pd.concat(response_dataframes).dropna().groupby(['date', 'parameter'], as_index=False)['aqi'].mean()
        #take AQI for 
        response_df = response_df.groupby(['date'], as_index = False)['aqi'].max()
    except Exception as e:
        logging.info(f"Data consolidation for year {year} failed with error {e}")
        response_df = None
    return response_df

def main():
    year_dfs = []
    for year in reversed(range(1961, 2022)):
        start_date = f"{year}0101"
        end_date = f"{year}1231"
        res_gas = request_daily_summary(param = AQI_PARAMS_GASEOUS,
                                        begin_date=start_date,
                                        end_date=end_date,
                                        api_key_store=api_key_store)
        res_particulates = request_daily_summary(param = AQI_PARAMS_PARTICULATES,
                                                begin_date=start_date,
                                                end_date=end_date,
                                                api_key_store=api_key_store)
        response_df = consolidate_results(res_gas, 
                                          res_particulates,
                                          year)
        year_dfs.append(response_df)
    full_dataframe = pd.concat(year_dfs)
    full_dataframe['year'] = pd.to_datetime(full_dataframe['date']).dt.year
    full_dataframe.to_csv(OUT_FILE, index = False)

if __name__ == "__main__":
    start = datetime.datetime.now()
    main()
    logging.info(f"Script has taken {datetime.datetime.now() - start} seconds to execute.")

