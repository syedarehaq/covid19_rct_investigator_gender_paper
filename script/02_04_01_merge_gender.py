# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from time import sleep
import pandas as pd
from collections import defaultdict, Counter
import json
import datetime
import codecs
# %%
pd.set_option('display.max_columns', 6)
pd.set_option('display.max_rows', 20)
pd.set_option('display.expand_frame_repr', True)
# %%
output_code = "02_04_01"
now = datetime.datetime.now().strftime("%Y%m%d")
# %%
## First read the dataframe of trials
trial_fname = "covid_trials_20200101_20200626"
df_trial_metadata = pd.read_csv("../input/raw/%s.csv" %(trial_fname))
df_trial_metadata["trial_id"] = df_trial_metadata["URL"].apply(lambda x: x.split("/")[-1])
# %%
## Read the previous data frame of roles with first name
df_role = pd.read_csv("../input/derived/%s_roles_with_genderizable_first_name_%s.csv" %("02_02_01",trial_fname))
# %%
## Now we are reading the gender of the first names that were derived from
## genedrize script 02_03_01
df_gender = pd.read_csv("../input/genderize/output/02_03_01_output_02_02_01_first_names_%s.csv" %trial_fname)
## We will only keep the detected male female gender of the names
df_gender = df_gender[df_gender["gender"]!="None"]
# %%
## Now merge the gender dataframe with role and then add the metadata of the 
## trials and create a combined dataframe
df_merged = df_role.merge(df_gender, on='first_name')
# %%
df_merged = df_merged.merge(df_trial_metadata, on="trial_id")
# %%
df_merged.to_csv("../input/derived/%s_trial_investigators_with_gender_and_metadata_%s.csv" %(output_code,trial_fname), index=False)