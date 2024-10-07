#!/bin/bash

#move into scripts directory
cd ${local_machine_scripts_directory}

#api call for desktop
python3 api_request.py desktop ${local_machine_data_directory} rare-disease_cleaned.AUG.2024.csv 

#api call for mobile web
python3 api_request.py mobile-web ${local_machine_data_directory} rare-disease_cleaned.AUG.2024.csv 

#api call for mobile app
python3 api_request.py mobile-app ${local_machine_data_directory} rare-disease_cleaned.AUG.2024.csv 

#merge mobile web and mobile app
python3 combine_api_results.py mobile-web mobile-app True mobile ${local_machine_data_directory} 

#merge desktop and mobile
python3 combine_api_results.py mobile desktop False cumulative ${local_machine_data_directory}