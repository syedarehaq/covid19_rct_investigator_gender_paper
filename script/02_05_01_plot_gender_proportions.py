# -*- coding: utf-8 -*-
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
output_code = "02_05_01"
now = datetime.datetime.now().strftime("%Y%m%d")
# %%
## First read the dataframe of trials
trial_fname = "type2diabetes_trials_2019010101_20191231" #"covid_trials_20200101_20200626"
df = pd.read_csv("../input/derived/%s_trial_investigators_with_gender_and_metadata_%s.csv" %("02_04_01",trial_fname))
dict_role_count = df["role"].value_counts().to_dict()
# %%
def func(pct, allvals):
    #absolute = int(pct/100.*np.sum(allvals))
    #return "{:.1f}% ({:d} )".format(pct, absolute)
    return "{:.1f} %".format(pct)
# %%
title_fontsize = 17
label_fontsize = 15
legend_fontsize = 14
#Create our plot and resize it.
explode = [0,0.05]
# %%
color_dict = {'male': '#e64550', 'female': '#1f97ce'}
fig,axarr = plt.subplots(1,3,figsize = (16,5))
sub_titles = ["A) Principal Investigators (%s)" %dict_role_count["Principal Investigator"],
                "B) Study Directors (%s)" %dict_role_count["Study Director"],
                "C) Study Chairs (%s)" %dict_role_count["Study Chair"]]
for i,count_type in enumerate(["Principal Investigator", "Study Director", "Study Chair"]):
    ax = axarr[i]
    df_current = df.loc[df["role"] == count_type,["gender"]]
    df_pie_chart = df_current["gender"].value_counts().reset_index().rename(columns={'index': 'gender', 0: 'count', "gender": count_type})
    print(count_type)
    print(df_pie_chart)
    genders, count = df_pie_chart["gender"].values, df_pie_chart[count_type].values
    colors = [color_dict[g] for g in genders]
    prob = np.array(count) / sum(count)
    
    #Create our plot and resize it.
    explode = [0,0.05]
    
    # borrowing from the following
    # https://www.machinelearningplus.com/plots/top-50-matplotlib-visualizations-the-master-plots-python/
    wedges, texts, autotexts = ax.pie(count, 
                                  autopct=lambda pct: func(pct, count),
                                  textprops=dict(color="w",size=20), 
                                  colors=colors,
                                  startangle=40,
                                  explode=explode)
    
    # Decoration
    if i == 2:
        ax.legend(wedges, [x.capitalize() for x in genders], loc="center left", bbox_to_anchor=(0.90, 0, 0.25, 1), fontsize = legend_fontsize+2)
    ax.set_title('%s' %sub_titles[i], y=0, x=0.5, fontsize = title_fontsize)
    #ax.set_title("A", loc = "bottom left")
    
    #Remove our axes and display the plot
    ax.axis('off')

trial_type = " ".join(trial_fname.split("trials")[0].strip().split("_")[:-1])
start_date = trial_fname.split("_")[-2]
end_date = trial_fname.split("_")[-1]
fig.suptitle("Gender (by roles) of the investigators of\n %s RCTs found in clinicaltrials.gov\n which are first posted between %s and %s" %(trial_type, start_date, end_date),fontsize=18)
now = datetime.datetime.now().strftime("%Y%m%d")
savefig_dir = "../output/"
#fig.tight_layout()
plt.savefig(savefig_dir+"%s_gender_pie_charts_%s_%s.png" %(output_code,trial_fname,now), dpi = 300)
plt.show()
