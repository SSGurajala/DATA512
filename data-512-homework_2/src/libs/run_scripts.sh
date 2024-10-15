#! /bin/bash

#move into local machine scripts directory
cd ${local_machine_scripts_directory}

#run page info api calls
python3 page_info_api_request.py ${initial_data_directory} ${pol_csv_file_name} ${revid_out_csv_file_name}

#run page info api calls
python3 ores_api_request.py ${intermediate_data_directory} ${revid_csv_out_file_name} ${pol_revid_out_file_name}