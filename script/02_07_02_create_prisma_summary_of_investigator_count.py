# -*- coding: utf-8 -*-
import pandas as pd
from collections import defaultdict, Counter
import json
import datetime
import codecs
import numpy as np
import matplotlib.pyplot as plt
# %%
pd.set_option('display.max_columns', 6)
pd.set_option('display.max_rows', 20)
pd.set_option('display.expand_frame_repr', True)
# %%
output_code = "02_07_02"
now = datetime.datetime.now().strftime("%Y%m%d")
#%%
all_trials = ["covid_trials_20200101_20200626",
            "breast_cancer_trials_20200101_20200626",
            "type2_diabetes_trials_20200101_20200626",
            "type2diabetes_trials_2019010101_20191231",
            "breast_cancer_trials_20190101_20191231"]
# %%
writelines = []
for trials_fname in all_trials:
    #trials_fname = "covid_trials_20200101_20200626"
    
    ## First get the total RCTs we have
    df_raw_trials = pd.read_csv("../input/raw/%s.csv" %(trials_fname))
    ## For some initial raw data download from clinicaltrials.gov I didn't include
    ## the NCT trial id column. For those I am generating it below
    if "trial_id" not in df_raw_trials.keys():
        df_raw_trials["trial_id"] = df_raw_trials["URL"].apply(lambda x: x.split("/")[-1])
    current_info_to_print = "There were initially %d trials found for %s" %(len(df_raw_trials), trials_fname)
    print(current_info_to_print)
    writelines.append(current_info_to_print)
    
    ## Then count the removed the  RCTs that do not have any investigator info
    ## Read the json file of investigator list and count how many of the RCTs have non empty list of investigators
    with open("../input/derived/02_01_01_investigators_%s.json" %(trials_fname), "r") as f:
        dict_trial_id_to_investigators = json.load(f)
    investigator_name_and_roles_by_trials = []
    for trial_id, investigaor_list in dict_trial_id_to_investigators.items():
        if investigaor_list:
            for investigaor_detail in investigaor_list:
                doc = investigaor_detail
                doc["trial_id"] = trial_id
                investigator_name_and_roles_by_trials.append(doc)
    dict_trial_id_to_investigators = {k:v for k,v in dict_trial_id_to_investigators.items() if v}
    current_info_to_print = "We have kept %d trials and removed %d" %(len(dict_trial_id_to_investigators), len(df_raw_trials) - len(dict_trial_id_to_investigators)) +\
                            " trials because they do not have any"+\
                            " investigator info in clinicaltrials.gov website."
    print(current_info_to_print)
    writelines.append(current_info_to_print)
    
    
    ## Then count the removed the RCTs whose investigators are organization or have no distinguishable name
    df_trials_with_genderizable_first_names = pd.read_csv("../input/derived/%s_roles_with_genderizable_first_name_%s.csv" %("02_02_01",trials_fname))
    current_info_to_print = "We have kept %d trials and removed %d" %(df_trials_with_genderizable_first_names["trial_id"].nunique(), len(dict_trial_id_to_investigators) - df_trials_with_genderizable_first_names["trial_id"].nunique()) +\
                            " trials as there is no distinguishable first name"+\
                            " because either the investigator first name is single letter"+\
                            " or the investigator is an organization"
    print(current_info_to_print)
    writelines.append(current_info_to_print)
    
    ## Then we have this many RCTs where there is at least one name of the investigator whose name could be genderized
    df_selected_final_trials = pd.read_csv("../input/derived/%s_trial_investigators_with_gender_and_metadata_%s.csv" %("02_04_01",trials_fname))
    current_info_to_print = "We have kept %d trials and removed %d" %(df_selected_final_trials["trial_id"].nunique(), df_trials_with_genderizable_first_names["trial_id"].nunique() - df_selected_final_trials["trial_id"].nunique()) +\
                            " trials because the first names we send to genderize API"+\
                            " could not return any identified gender"
    print(current_info_to_print)
    writelines.append(current_info_to_print)
# %%
with open("../output/%s_prisma_style_summary_of_all_trials.txt" %(output_code), "w") as f:
        f.writelines("\n".join(writelines))
#%%
## First get the total RCTs we have
## Then remove the  RCTs that do not have any investigator info
## Then remove the RCTs whose investigators are organization
## Then remove the RCTs where there is not at least one investigator whose name could be genderized
## Then we have this many RCTs where there is at least one name of the investigator whose name could be genderized
## Finally we have:
    ## This many Principal Investigators
    ## This many Study Directors
    ## This many Study Chairs
    