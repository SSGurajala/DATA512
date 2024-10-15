import json, urllib, time
import pandas as pd
import sys
import logging
import datetime
import requests 
import os

start = datetime.datetime.now()
#set up logging 
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=f"../../logs/pageinfo_api_requests.log")

#assign access and output file path variables 
data_dir = str(sys.argv[1])
csv_file_name = str(sys.argv[2])
out_file_name = str(sys.argv[3])

out_file = os.path.join(data_dir, out_file_name)
csv_file = pd.read_csv(os.path.join(data_dir, csv_file_name))

###############
###CONSTANTS###
###############

# The basic English Wikipedia API endpoint
API_ENWIKIPEDIA_ENDPOINT = "https://en.wikipedia.org/w/api.php"
API_HEADER_AGENT = 'User-Agent'

# We'll assume that there needs to be some throttling for these requests - we should always be nice to a free data resource
API_LATENCY_ASSUMED = 0.002       # Assuming roughly 2ms latency on the API and network
API_THROTTLE_WAIT = (1.0/100.0)-API_LATENCY_ASSUMED

# When making automated requests we should include something that is unique to the person making the request
# This should include an email - your UW email would be good to put in there
REQUEST_HEADERS = {
    'User-Agent': '<sgura99@uw.edu>, University of Washington, MSDS DATA 512 - AUTUMN 2024'
}

# This template lists the basic parameters for making this
PAGEINFO_PARAMS_TEMPLATE = {
    "action": "query",
    "format": "json",
    "titles": "",           # to simplify this should be a single page title at a time
    "prop": "info",
    "inprop": ""
}

def pageinfo_api_call(article_title = None, 
                      endpoint_url = API_ENWIKIPEDIA_ENDPOINT, 
                      request_template = PAGEINFO_PARAMS_TEMPLATE,
                      headers = REQUEST_HEADERS,
                      failed_response_counter=0):
    #set article title if supplied
    if article_title:
        request_template['titles'] = article_title
    #raise error for no article title
    if not request_template['titles']:
        raise Exception("Must supply an article title to make a pageinfo request.")
        logging.info("API Call failed because valid article title not provided")

    # make the request
    try:
        #throttling 
        if API_THROTTLE_WAIT > 0.0:
            time.sleep(API_THROTTLE_WAIT)
        #make response 
        response = requests.get(endpoint_url, headers=headers, params=request_template)
        #raise status errors 
        response.raise_for_status()
        #convert to json and log
        json_response = response.json()
        logging.info(f"API Call succeeded for article titles {article_title}")
    except Exception as e:
        #log error as needed 
        json_response = None
        logging.info(f"API Call Failed for article titles {article_title} due to error {e}")
        #update failed response counter
        failed_response_counter += 1

    return json_response, failed_response_counter


def main(csv_file = csv_file, 
         out_file = out_file, 
         start = start):
    #initialize list of article titles
    article_titles = csv_file.name
    #empty list to append to
    df_list = []
    #failure case counters
    failed_response_counter = 0
    no_rev_id_counter = 0
    #loop through article titles
    for article in article_titles:
        res, failed_response_counter = pageinfo_api_call(article, failed_response_counter=failed_response_counter)
        key = list(res['query']['pages'].keys())[0]
        value = res['query']['pages'][key]
        if value and 'lastrevid' in value.keys():
            df_list.append(pd.DataFrame({"article_title" : [value['title']],
                                            "revision_id" : [value['lastrevid']]}))     
        else:
            logging.info(f"No revision id available for article {value['title']}!")    
            no_rev_id_counter += 1       
    #make df
    df = pd.concat(df_list)
    #write csv
    df.to_csv(out_file, index = False)
    #logging statements
    logging.info(f"A total of {failed_response_counter} API Calls failed to execute succesfully.")
    logging.info(f"A total of {no_rev_id_counter} articles did not have a revision ID available for the given parameters.")
    end = datetime.datetime.now()
    logging.info(f"Run took {end - start} total seconds!") 

#execute main function
if __name__ == "__main__":
    main()