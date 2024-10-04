import json, time, urllib
import pandas as pd
from aiohttp import ClientSession
import asyncio
import sys
import datetime 

#assign acess and output file path variables 
access = str(sys.argv[1])
data_dir = str(sys.argv[2])
output_file_path = str(sys.argv[3])
csv_file_path = str(sys.argv[4])
#read in dataframe
rare_disease_df = pd.read_csv(data_dir + csv_file_path)
#assign article titles 
article_titles = rare_disease_df.disease


# The REST API 'pageviews' URL - this is the common URL/endpoint for all 'pageviews' API requests
API_REQUEST_PAGEVIEWS_ENDPOINT = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/'

# This is a parameterized string that specifies what kind of pageviews request we are going to make
# In this case it will be a 'per-article' based request. The string is a format string so that we can
# replace each parameter with an appropriate value before making the request
API_REQUEST_PER_ARTICLE_PARAMS = 'per-article/{project}/{access}/{agent}/{article}/{granularity}/{start}/{end}'

# The Pageviews API asks that we not exceed 100 requests per second, we add a small delay to each request
API_LATENCY_ASSUMED = 0.002       # Assuming roughly 2ms latency on the API and network
API_THROTTLE_WAIT = (1.0/100.0)-API_LATENCY_ASSUMED

# When making a request to the Wikimedia API they ask that you include your email address which will allow them
# to contact you if something happens - such as - your code exceeding rate limits - or some other error 
REQUEST_HEADERS = {
    'User-Agent': 'sgura99@uw.edu, University of Washington, MSDS DATA 512 - AUTUMN 2024',
}
# This template is used to map parameter values into the API_REQUST_PER_ARTICLE_PARAMS portion of an API request. The dictionary has a
# field/key for each of the required parameters. In the example, below, we only vary the article name, so the majority of the fields
# can stay constant for each request. Of course, these values *could* be changed if necessary.
ARTICLE_PAGEVIEWS_PARAMS_TEMPLATE = {
    "project":     "en.wikipedia.org",
    "access":      "",      # this should be changed for the different access types
    "agent":       "user",
    "article":     "",             # this value will be set/changed before each request
    "granularity": "monthly",
    "start":       "2015070100",   # start and end dates need to be set
    "end":         "2024093000"    # this is likely the wrong end date
}



def format_url(article_title,
                base_endpoint_url, 
                endpoint_params,
                request_template,
                access):
    #replace article title in template
    if article_title:
        request_template['article'] = article_title
    #check for template
    if not request_template['article']:
        raise Exception("Must supply an article title to make a pageviews request.")

    # Titles are supposed to have spaces replaced with "_" and be URL encoded
    article_title_encoded = urllib.parse.quote(request_template['article'].replace(' ','_'))
    request_template['article'] = article_title_encoded
    request_template["access"] = access
    
    # now, create a request URL by combining the endpoint_url with the parameters for the request
    request_url = base_endpoint_url+endpoint_params.format(**request_template)
    return request_url

async def api_request(request_url, 
                      session):
    
    # Check for request URL 
    if not request_url:
        raise Exception("Must supply a request URL to make an api request.")
    try:
        #Time sleep the throttle wiat 
        time.sleep(API_THROTTLE_WAIT)
        #Await responses
        response = await session.get(request_url)
        #Await json serialization
        response = await response.json()
    except:
        response = None
    return response

async def get_page_views(article_title,
                        base_endpoint_url, 
                        endpoint_params,
                        request_template,
                        headers,
                        access):
    #format URL 
    request_url = format_url(article_title, 
                             base_endpoint_url,
                             endpoint_params,
                             request_template,
                             access)
    #Make session
    session = ClientSession(headers=headers)
    #Await api request 
    response = await api_request(request_url,
                                 session)
    #close session
    await session.close()
    #remove access key in response
    try:
        for iter in response['items']:
            del iter['access']
    except:
        response = None
    return article_title, response    

async def main():
    #initialize page view results
    page_view_res = {}
    #create async tasks for api calls
    tasks = [asyncio.create_task(get_page_views(url,
                                                API_REQUEST_PAGEVIEWS_ENDPOINT,
                                                API_REQUEST_PER_ARTICLE_PARAMS,
                                                ARTICLE_PAGEVIEWS_PARAMS_TEMPLATE,
                                                REQUEST_HEADERS,
                                                access)) for url in article_titles]
    #gather all tasks
    responses = await asyncio.gather(*tasks)
    #assign title as keys and items of json obj
    for response in responses:
        title, json_obj = response
        if json_obj:
            page_view_res[title] = json_obj['items']
    out_file_path = data_dir + output_file_path 
    #write file 
    with open(out_file_path, 'w') as file:
        json.dump(page_view_res, file)

asyncio.run(main())