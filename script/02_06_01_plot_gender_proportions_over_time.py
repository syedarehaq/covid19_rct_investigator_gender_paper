# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from time import sleep
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
output_code = "02_06_01"
now = datetime.datetime.now().strftime("%Y%m%d")
# %%
## First read the dataframe of trials
trial_fname = "type2_diabetes_trials_20200101_20200626"
analysis_type = "week"
bar_type = "count" # "count" , "prob"
df = pd.read_csv("../input/derived/%s_trial_investigators_with_gender_and_metadata_%s.csv" %("02_04_01",trial_fname))
dict_role_count = df["role"].value_counts().to_dict()
# %%
## Some of the dates do not have details, we will ignore then when getting specific date and specific week, but we will keep them for the month
def validate_dates_in_the_dataset(s):
    if len(s.split(","))>1:
        return True
## This preprocess is required for this exception date string
## ValueError: time data 'April 13, 2020' does not match format '%B %d,%Y'
def preprocess_date_string(s):
    return s.replace(", ",",")

def get_date_from_a_string_datetime(s):
    if s:
        s = preprocess_date_string(s)
        if validate_dates_in_the_dataset(s):
            ts = datetime.datetime.strptime(s,"%B %d,%Y")
            return ts.strftime("%Y-%m-%d")
        else:
            return None
    else:
        return None
    
def get_week_from_a_string_datetime(s):
    if s:
        s = preprocess_date_string(s)
        if validate_dates_in_the_dataset(s):
            ts= datetime.datetime.strptime(s,"%B %d,%Y")
            return "%d-%02d" %(ts.year,ts.isocalendar()[1])
        else:
            return None
    else:
        return None
    
def get_month_from_a_string_datetime(s):
    if s:
        s = preprocess_date_string(s)
        month_to_string = {'May 2020': "2020-05",
         'June 2020': "2020-06",
         'April 2020': "2020-04",
         'March 2020': "2020-03",
         'November 2020': "2020-11"}
        if validate_dates_in_the_dataset(s):
            ts = datetime.datetime.strptime(s,"%B %d,%Y")
            return "%d-%02d" %(ts.year,ts.month)
        else:
            return month_to_string[s]
    else:
        return None
# %%
df["first_post_date"] = df["First Posted"].apply(lambda x: get_date_from_a_string_datetime(x))
df["first_post_week"] = df["First Posted"].apply(lambda x: get_week_from_a_string_datetime(x))
df["first_post_month"] = df["First Posted"].apply(lambda x: get_month_from_a_string_datetime(x))

# %%
title_fontsize = 17
label_fontsize = 15
legend_fontsize = 14
#Create our plot and resize it.
explode = [0,0.05]
# %%
color_dict = {'male': '#1f97ce', 'female': '#e64550'}
palette_male_female = color_dict.values()
df_analysis_column = "first_post_%s" %analysis_type
## df_analysis_column = "start_week"
## Removing the rows where the week is None
df_plot = df[df[df_analysis_column].notnull()]
print(df_plot["trial_id"].nunique())

## Plotting
fig,ax = plt.subplots(1,1,figsize = (15,5))
df_bar = df_plot.groupby([df_analysis_column,"gender"]).size().rename('count')

if bar_type == "prob":
    df_bar = df_bar / df_bar.groupby(level=0).sum()
df_bar = df_bar.to_frame().reset_index()
df_bar = df_bar.pivot(df_analysis_column,"gender","count").fillna(0)

flattened = pd.DataFrame(df_bar.to_records())
ax = flattened.plot(x=df_analysis_column,ax=ax, kind='bar', stacked=True, mark_right=True, color=palette_male_female)

trial_type = " ".join(trial_fname.split("trials")[0].strip().split("_")[:-1])
start_date = trial_fname.split("_")[-2]
end_date = trial_fname.split("_")[-1]
ax.set_title("Gender of investigators over time (trial first post %ss) of\n%s RCTs found in clinicaltrials.gov\n which are first posted between %s and %s" %(analysis_type, trial_type, start_date, end_date), fontsize = title_fontsize)

## Legend stuffs 
# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
lgd = ax.legend(["Female","Male"],loc='center left', bbox_to_anchor=(1, 0.5), fontsize = legend_fontsize)


## x-axis stuffs
ax.xaxis.label.set_visible(False)
x_ticklabels = [l.get_text().title() for l in ax.xaxis.get_ticklabels()]
ax.set_xticklabels(x_ticklabels, fontsize = label_fontsize)

## x-axis stuffs
ax.tick_params(axis="y", labelsize=label_fontsize)

plt.tight_layout()
plt.savefig("../output/%s_gender_proportion_over_first_post_%ss_%s_%s_%s.png" %(output_code,analysis_type,trial_fname,bar_type,now), bbox_extra_artists=[lgd], bbox_inches='tight')
plt.show()