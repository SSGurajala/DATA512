import json, urllib, time
import pandas as pd
import sys
import os
import logging
import datetime
import requests

from api_key_store import API_KEY_STORE

#Initialize Key Store so access tokens will not be exposed
api_key_store = API_KEY_STORE("enwiki-articlequality")


start = datetime.datetime.now()
#set up logging 
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=f"../../logs/ores_api_requests.log")

#assign access and output file path variables 
data_dir = str(sys.argv[1])
csv_file_name = str(sys.argv[2])
out_file_name = str(sys.argv[3])

out_file = os.path.join(data_dir, out_file_name)
csv_file = pd.read_csv(os.path.join(data_dir, csv_file_name))

#########
#
#    CONSTANTS
#
#    The throttling rate is a function of the Access token that you are granted when you request the token. The constants
#    come from dissecting the token and getting the rate limits from the granted token. An example of that is below.
#
API_LATENCY_ASSUMED = 0.002       # Assuming roughly 2ms latency on the API and network
API_THROTTLE_WAIT = ((60.0*60.0)/5000.0)-API_LATENCY_ASSUMED  # The key authorizes 5000 requests per hour

#    When making automated requests we should include something that is unique to the person making the request
#    This should include an email - your UW email would be good to put in there
#    
#    Because all LiftWing API requests require some form of authentication, you need to provide your access token
#    as part of the header too
#
REQUEST_HEADER_TEMPLATE = {
    'User-Agent': "<{email_address}>, University of Washington, MSDS DATA 512 - AUTUMN 2024",
    'Content-Type': 'application/json',
    'Authorization': "Bearer {access_token}"
}
#
#    This is a template for the parameters that we need to supply in the headers of an API request
#
REQUEST_HEADER_PARAMS_TEMPLATE = {
    'email_address' : "",         # your email address should go here
    'access_token'  : ""          # the access token you create will need to go here
}

#
#    This is a template of the data required as a payload when making a scoring request of the ORES model
#
ORES_REQUEST_DATA_TEMPLATE = {
    "lang":        "en",     # required that its english - we're scoring English Wikipedia revisions
    "rev_id":      "",       # this request requires a revision id
    "features":    True
}

### FUNCTIONS

def make_ores_api_call(article_revid = None,
                        api_key_store = None,
                        request_data = ORES_REQUEST_DATA_TEMPLATE,
                        header_format = REQUEST_HEADER_TEMPLATE,
                        header_params = REQUEST_HEADER_PARAMS_TEMPLATE,
                        request_wait_timing = API_THROTTLE_WAIT):

    request_data['rev_id'] = article_revid
    header_params['email_address'] = api_key_store.WIKIMEDIA_EMAIL_ADDRESS
    header_params['access_token'] = api_key_store.WIKIMEDIA_ACCESS_TOKEN

    if not article_revid:
            raise Exception("Must provide a valid article revision ID")
            logging.info("API Call failed: Valid article revision ID not Provided!")
    if not header_params["email_address"]:
        raise Exception("Must provide valid api key store object. Email Address Not Available.")
        logging.info("API Call Failed: Valid API Key Store Object not Provided! Email Address Not Available.")
    if not header_params["access_token"]:
        raise Exception("Must provide valid api key store object. Access Token Not Available.")
        logging.info("API Call Failed: Valid API Key Store Object not Provided! Access Token Not Available.")

    # Create a compliant request header from the template and the supplied parameters
    headers = dict()
    for key in header_format.keys():
        headers[str(key)] = header_format[key].format(**header_params)

    try:
        time.sleep(request_wait_timing)
        response = requests.post(api_key_store.WIKIMEDIA_ORES_ENDPOINT, headers=headers, data=json.dumps(request_data))

        
        response.raise_for_status()

        json_response = response.json() 
        logging.info(f"ORES API Call for Article Revision ID {article_revid} succeeded!")

    except Exception as e:

        logging.info(f"ORES API Call for Article Revision ID {article_revid} failed with reason: {e}")
        json_response = None 

    return article_revid, json_response

def parse_api_response(api_response_json):
    scores_dict = api_response_json['enwiki']['scores']
    scores_key = list(scores_dict.keys())[0]
    prediction = scores_dict[scores_key]['articlequality']['score']['prediction']
    return prediction 

def main(api_key_store=api_key_store,
            csv_file=csv_file,
            out_file=out_file):
    
    revids = csv_file.revision_id.tolist()
    #init response list 
    responses = []
    for revision_id in revids:
        responses.append(make_ores_api_call(article_revid = int(revision_id),
                                            api_key_store= api_key_store))
    #assign title as keys and items of json obj
    formatted_response_list = []
    response_failed_count = 0
    for response in responses:
         article_revision_id, json_response = response
         if json_response:
            prediction = parse_api_response(json_response)
            formatted_response_list.append(pd.DataFrame({"revision_id" : [article_revision_id],
                                                         "article_quality" : [prediction]}))
         else:
            response_failed_count += 1
    response_dataframe = pd.concat(formatted_response_list)
    response_dataframe.to_csv(out_file)

    end = datetime.datetime.now()
    logging.info(f"This run took {end - start} seconds to complete!")
    logging.info(f"{response_failed_count} api calls failed.")

if __name__ == "__main__":
    main()       







