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
output_code = "02_07_01"
now = datetime.datetime.now().strftime("%Y%m%d")
#%%
all_trials = ["covid_trials_20200101_20200626",
            "breast_cancer_trials_20200101_20200626",
            "type2_diabetes_trials_20200101_20200626",
            "type2diabetes_trials_2019010101_20191231",
            "breast_cancer_trials_20190101_20191231"]
# %%
for trials_fname in all_trials:
    writelines = []
    ## First read the dataframe of trials
    df_raw_trials = pd.read_csv("../input/raw/%s.csv" %(trials_fname))
    ## For some initial raw data download from clinicaltrials.gov I didn't include
    ## the NCT trial id column. For those I am generating it below
    if "trial_id" not in df_raw_trials.keys():
        df_raw_trials["trial_id"] = df_raw_trials["URL"].apply(lambda x: x.split("/")[-1])
    writelines.append("There were initially %d trials found for %s" %(len(df_raw_trials), trials_fname))
    df_selected_trials = pd.read_csv("../input/derived/%s_trial_investigators_with_gender_and_metadata_%s.csv" %("02_04_01",trials_fname))
    writelines.append("Among them we have kept %d trials." %(df_selected_trials["trial_id"].nunique())+
        "The other %d trials could not be kept because either there were no investigators," %(len(df_raw_trials) - df_selected_trials["trial_id"].nunique())+
        " or the investigator was an organization, or the name could not be genderized. Below are the links to the trials those were not included:\n\n")
    example_trials_not_included = ["trial_url"]+["https://clinicaltrials.gov/ct2/show/"+x for x in list(set(df_raw_trials["trial_id"]) - set(df_selected_trials["trial_id"]))]
    example_trials_not_included = "\n".join(example_trials_not_included)
    #print(example_trials_not_included)
    with open("../output/%s_summary_of_trials_not_included_%s.txt" %(output_code,trials_fname), "w") as f:
        f.writelines("\n".join(writelines))
        f.writelines(example_trials_not_included)
    # %%
    print("\n".join(writelines))