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
output_code = "02_02_01"
now = datetime.datetime.now().strftime("%Y%m%d")
# %%
trial_fname = "covid_trials_20200101_20200626"
# %%
## Now loading the names 
with open("../input/derived/02_01_01_investigators_%s.json" %(trial_fname), "r") as f:
    dict_trial_id_to_investigators = json.load(f)
# %%
investigator_name_and_roles_by_trials = []
for trial_id, investigaor_list in dict_trial_id_to_investigators.items():
    if investigaor_list:
        for investigaor_detail in investigaor_list:
            doc = investigaor_detail
            doc["trial_id"] = trial_id
            investigator_name_and_roles_by_trials.append(doc)
# %%
df_role = pd.DataFrame(investigator_name_and_roles_by_trials)
df_role["role"] = df_role["role"].apply(lambda x: x.replace(":",""))
print(df_role["role"].value_counts())
dict_role_count = df_role["role"].value_counts().to_dict()

# %%
## Now some preprocessing of the names
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever
def process_name(name):
    name_lower = name.lower()
    name_lower = remove_prefix(name_lower,"assoc.")
    name_lower = remove_prefix(name_lower,"dr.")
    name_lower = remove_prefix(name_lower,"dr ")
    name_lower = remove_prefix(name_lower,"co-pi:")
    name_lower = remove_prefix(name_lower,"m.sc.")
    name_lower = remove_prefix(name_lower,"prof ")
    name_lower = remove_prefix(name_lower,"prof.")
    ## I repeated this dr. portion intentionally to catch cases like
    ## assoc. prof. dr. barakatun nisak
    name_lower = remove_prefix(name_lower,"dr.")
    name_lower = name_lower.split(",")[0]
    name_lower = name_lower.lstrip()
    return name_lower

# %%
df_role["processed_name"] = df_role["name"].apply(lambda x: process_name(x))
# %%
#print("\n".join(sorted(set(df_role["processed_name"].values))[:200]))
print("Before Removal\n--------------------")
print("\n".join(sorted(set(df_role["processed_name"].values))))
# %%
## Now by invetigating the names by hand printed above, we have found some names
## that are not human names, we are removing them.

non_human_entity = ["70-4665-9174 70-4665-9174",\
                    'abbvie inc.',\
                    'biontech responsible person',\
                    'call 1-877-ctlilly (1-877-265-4559 or 1-317-615-4559) mon - fri 9am - 5pm eastern time (utc/gmt - 5 hours',\
                    "call 1-877-ctlilly (1-877-285-4559) or 1-317-615-4559 mon - fri 9 am - 5 pm eastern time (utc/gmt - 5 hours",\
                    "call 1-877-ctlilly (1-877-285-4559) or1-317-532-0186 mon - fri 9 am - 5 pm eastern time (utc/gmt - 5 hours",\
                    "call 1-877-ctlilly (1-877-285-4559) or 1-317-532-0186 mon - fri 9 am - 5 pm eastern time (utc/gmt - 5 hours",\
                    "cancer trials ireland dublin 11",\
                    "chief medical investigator",\
                    "chief technical officer",\
                    "china medicine university",\
                    "clinical development chief medical and scientific officer",\
                    "clinical reporting anchor & disclosure (1452)",\
                    "clinical reporting anchor and disclosure (1452)",\
                    'clinical sciences & operations',\
                    'clinical trial management',\
                    'clinical trials',\
                    "fudan university shanghai cancer center",\
                    'gilead study director',\
                    "gsk clinical trials",\
                    "johnson & johnson private limited clinical trial",\
                    "immunomedics medical director",\
                    "md",\
                    "medical director",\
                    'pfizer ct.gov call center',\
                    'sbmu',
                    "shanghai institute of biological products co.",\
                    "study director",\
                    "s.kuemmel@kem-med.com kuemmel",\
                    
                   ]
## So the rule is
## We are removing all these non-human entities
## Then we are also removeing any entity such as "a. thomas stavros",
## "a e van leeuwen- stok", because the first name is single letter after
## removeal of the dot, or even without removing any dot.
print("Before removal of the non human entities we had in total %d entities" %(len(df_role)))
df_role = df_role[~df_role["processed_name"].isin(non_human_entity)].copy()
print("After Removal\n--------------------")
print("\n".join(sorted(set(df_role["processed_name"].values))))
print("After removal of the non human entities we have in total %d entities" %(len(df_role)))

## Now we are removing the names who are single letter, e.g. "a. thomas stavros"
## or "a e van leeuwen- stok"
df_role["first_name"] = df_role["processed_name"].apply(lambda x: x.split()[0].replace(".",""))
df_role = df_role[df_role["first_name"].str.len() > 1].copy()
print("After removal of the single letter first name",\
      "entities we have in total %d entities" %(len(df_role)))
# %%
## Now we are saving the file to create input for genderization process
with open("../input/genderize/input/%s_first_names_%s.csv" %(output_code,trial_fname), "w") as f:
    f.writelines("\n".join(sorted(set(df_role["first_name"].values))))

# %%
## We are also saving the the role dataframe for future use in merging the genders
## of the investigators with other trial metadata
df_role.to_csv("../input/derived/%s_roles_with_genderizable_first_name_%s.csv" %(output_code,trial_fname), index=False)