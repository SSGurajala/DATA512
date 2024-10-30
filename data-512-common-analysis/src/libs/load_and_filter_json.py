import sys
from helpers import *
import os
import time
import logging 
import json
import multiprocessing
import geojson
from datetime import datetime
import re
os.chdir(os.getenv("DATA512_BASE_FILE_PATH"))

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=f"./logs/geojson_loading.log")

DATA_FILE = "data/USGS_Wildland_Fire_Combined_Dataset.json"
OUT_FILE = "data/USGS_Wildland_Fire_Combined_Dataset_filtered.json"

#coords of dearborn MI
coords = [42.322262, -83.176315]


def load_and_filter_year_geojson(feature, coords = coords):
    """
    Filter function that operates on features. 
    """
    #assign ring data
    if 'rings' in feature['geometry']:
        ring_data = feature['geometry']['rings'][0]
    elif 'curveRings' in feature['geometry']:
        ring_data = feature['geometry']['curveRings'][0]
    else:
        feature = None
    try:
        #check fire year
        if feature['attributes']['Fire_Year'] >= 1961 and feature['attributes']['Fire_Year'] < 2022:
            distance = shortest_distance_from_place_to_fire_perimeter(coords, ring_data)
            #filter on distance
            if distance[0] <= 1800:
                feature['attributes']['Distance_to_DearbornMI'] = distance[0]
                logging.info(f"Fire {feature['attributes']['Listed_Fire_Names']} is included!.")
        #otherwise set feature to be none
            else:
                feature = None
        else:
            feature = None
    except Exception as e:
        logging.info(f"Error for Fire {feature['attributes']['Listed_Fire_Names']}:{e}")
        feature = None
    return feature

def main():
    #Open file 
    geojson_file = open(DATA_FILE,"r")
    gj_data = geojson.load(geojson_file)
    #read in data
    logging.info("Data Read in!")
    #
    features = gj_data['features']
    filtered_features= []
    feature_number = 0
    for feature in features:
        feature = load_and_filter_year_geojson(feature)
        feature_number += 1
        if feature:
            filtered_features.append(feature['attributes'])
        if feature_number % 10000 == 0:
            logging.info(f"Processed and filtered {feature_number} number of features sofar.")
    with open(OUT_FILE, "w") as output_file:
        json.dump(filtered_features, output_file)
    logging.info(f"A total of {len(filtered_features)} written.")

if __name__ == "__main__":
    start = datetime.now()
    main() 
    logging.info(f"Script has taken {datetime.now() - start} seconds to execute!")
