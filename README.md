The genderize.io API and the API key used is bought and found here in this link : https://store.genderize.io
Create a directory called `api_keys/genderize.txt` above this directory and put the genderize api key in the `genderize.txt` file.

All the different type of trials that was collected using keywords and timeline restrictions from the clinicaltrials.gov can be found in the directory `./input/raw`.

These raw trials are used for collecting the gender information using genderize.io api, the script used to that step by step are:
- ./script/02_01_01_scrape_investigator_role_name_nct_from_csv.py
- ./script/02_02_01_create_first_names_for_genderization.py
- ./script/02_03_01_get_genders.py
- ./script/02_04_01_merge_gender.py

Finally the all plots and results created are in the folder called `./output`. The scripts that genderated these results and plots are:
- ./script/02_05_01_plot_gender_proportions.py
- ./script/02_06_01_plot_gender_proportions_over_time.py
- ./script/02_07_01_create_summary_of_investigator_count.py
- ./script/02_07_02_create_prisma_summary_of_investigator_count.py
