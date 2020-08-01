All the different type of trials that was collected using keywords and timeline restrictions from the clinicaltrials.gov can be found in the directory `./raw`.

These raw trials are used for collecting the gender information using genderize.io api, the script used to that step by step are:
- ./scripts/02_01_01_scrape_investigator_role_name_nct_from_csv.py
- ./scripts/02_02_01_create_first_names_for_genderization.py
- ./scripts/02_03_01_get_genders.py
- ./scripts/02_04_01_merge_gender.py

Finally the all plots and results created are in the folder called `./output`. The scripts that genderated these results and plots are:
- ./scripts/02_05_01_plot_gender_proportions.py
- ./scripts/02_06_01_plot_gender_proportions_over_time.py
- ./scripts/02_07_01_create_summary_of_investigator_count.py
- ./scripts/02_07_02_create_prisma_summary_of_investigator_count.py