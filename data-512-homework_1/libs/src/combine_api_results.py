import json
import sys 
from collections import Counter, defaultdict
import pandas as pd
import os
import logging
import datetime 

start_time = datetime.datetime.now()

#assign access and output file path variables 
access1 = str(sys.argv[1])
access2 = str(sys.argv[2])
#do we want to delete originals or no
delete_originals = bool(sys.argv[3] == "True")
out_access = str(sys.argv[4])
data_dir = str(sys.argv[5])

#start and end for path strings
start = "2015070100"
end = "2024093000"

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=f"../../logs/combine_api_results_{access1}_{access2}.log")

#format output file path
out_file_path = f"{data_dir}/rare-disease_monthly_{out_access}_{start}-{end}.json"

#format json paths
access1_json_path = f"{data_dir}/rare-disease_monthly_{access1}_{start}-{end}.json"
access2_json_path = f"{data_dir}/rare-disease_monthly_{access2}_{start}-{end}.json"

#load json objects
with open(access1_json_path, "r") as file:  
    access1_json = json.load(file)

with open(access2_json_path, "r") as file:  
    access2_json = json.load(file)

#put lists together per key to get all timestamps from both sources in same list
merged_json = {}
for title in access1_json.keys():
    merged_json[title] = access1_json[title] + access2_json[title]

#function to sum views for the same articles timestamps
def sum_unique_views_output_dict(merged_json_object):
    #initalize default dict of lists for output
    result_dict = defaultdict(list)
    #loop through list of api results (now with two entries per timestamp)
    for article, api_result_list in merged_json_object.items():
        #initialize default view tracker dictionary per timestamp
        view_tracker = defaultdict(lambda : {
                'project' : None,
                'granularity' : None,
                'agent' : None,
                'views' : 0,
        })
        #loop through every item in the list of resutls 
        for list_iter in api_result_list:
            #intialize the timestamp
            timestamp = list_iter['timestamp']
            #add the views from a given timestamp
            view_tracker[timestamp]['views'] += list_iter['views']
            #source other info from the iteration of the list if not already set
            if view_tracker[timestamp]['agent'] is None:
                view_tracker[timestamp]['project'] = list_iter['project']
                view_tracker[timestamp]['granularity'] = list_iter['granularity']
                view_tracker[timestamp]['agent'] = list_iter['agent']
        #add summed monthly entry to high level output dict
        for timestamp, monthly_entry_info in view_tracker.items():
            result_dict[article].append({
                'project' :  view_tracker[timestamp]['project'],
                'article' : article,
                'granularity' : view_tracker[timestamp]['granularity'],
                'timestamp' : timestamp,
                'agent' : view_tracker[timestamp]['agent'],
                'views' : view_tracker[timestamp]['views']
            })
        logging.info(f"Result merging has finished for article {article}")
    #convert from default dict to dict
    return dict(result_dict)

def run_merge(merged_json, delete_originals=False):
    output_json = sum_unique_views_output_dict(merged_json)
    with open(out_file_path, 'w') as file:
        json.dump(output_json, file)
    if delete_originals:
        os.remove(access1_json_path)
        os.remove(access2_json_path)
        logging.info(f"Temp Files {access1_json_path} and {access2_json_path} removed.")
def main():
    run_merge(merged_json,
              delete_originals)
    end_time = datetime.datetime.now() 
    logging.info(f"Total Run took {end_time - start_time} seconds!")
    
main()