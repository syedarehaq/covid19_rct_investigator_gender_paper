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
output_code = "02_01_01"
now = datetime.datetime.now().strftime("%Y%m%d")
# %%
def get_role_name_aff_address_from_tr(tr):
    if tr.find(id="role"): 
        if tr.find(id="role")["style"] == "visibility:hidden":
            return None
    else:
        doc = {}
        for td in tr.find_all("td"):
            doc[td["headers"][0]] = td.text
        return doc
# %%
trial_list_file = "type2_diabetes_trials_20200101_20200626"
df = pd.read_csv("../input/raw/%s.csv" %trial_list_file)
# %%
df["ID"] = df["URL"].apply(lambda x: x.split("/")[-1])
# %%
trial_id_to_investigators = defaultdict(list)
# %%
dict_trial_id_to_url = df.set_index("ID").to_dict()["URL"]
# %%
count = 0
for trial_id, url in dict_trial_id_to_url.items():
    count += 1
    if count % 10 == 0:
        print("%d out of %d" %(count, len(dict_trial_id_to_url)))
    #trial_id = "NCT04372979"
    #url = 'https://ClinicalTrials.gov/show/NCT04372979'
    
    ## We are interested about the contacts only
    url_contact = url + "#contacts"
    index = requests.get(url).text
    soup = BeautifulSoup(index, 'html.parser')
    ## We are interested about the investigatros only
    ## source: https://stackoverflow.com/questions/44893862/find-specific-table-using-beautifulsoup-with-specific-caption
    table = None
    for caption in soup.find_all('caption'):
        if caption.get_text() == 'Layout table for investigator information':
            table = caption.find_parent('table', {'class': 'ct-layout_table tr-indent2'})
    if table:
        ## So in this example we sometime have a specific trs that we are looking for
        ## inside a tbody and sometime if ther is a single element then there is
        ## tbody. So we will get all trs instead and discard the ones where the role is
        ## invisible
        trs = table.find_all("tr")
        ## For each tr give it to the get role name aff fucntion and it should return 
        ## possible role name json if any is there are  is not invisible
        for tr in trs:
            role_name_doc = get_role_name_aff_address_from_tr(tr)
            if role_name_doc:
                trial_id_to_investigators[trial_id].append(role_name_doc)
    if trial_id not in trial_id_to_investigators:
        trial_id_to_investigators[trial_id] = None
    sleep(1)
# %%
## https://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence
with codecs.open("../input/derived/%s_investigators_%s.json" %(output_code,trial_list_file),"w",  encoding='utf-8') as f:
    json.dump(trial_id_to_investigators,f,ensure_ascii=False)