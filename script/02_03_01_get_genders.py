from genderize import Genderize
from time import sleep
# %%
plot_code = "02_03_01"
# %%

## genderizer_api_output = Genderize().get(['James', 'Eva', 'Thunderhorse'])
with open("../../api_keys/genderize.txt","r") as  f:
	key = f.readline()

genderize = Genderize(user_agent='GenderizeDocs/0.0',
	api_key=key,
	timeout=5.0)
# %%
open_dir = "../input/genderize/input/"
trial_name = "covid_trials_20200101_20200626"
open_file = "02_02_01_first_names_%s" %trial_name
#chunk_num = 0
open_fname = open_dir+"%s.csv" %(open_file)
valid_first_names = []
with open(open_fname,"r") as f:
	for line in f:
		valid_first_names.append(line.strip())
writelines = []
writelines.append(",".join(["first_name","gender","gender_probability","gender_sample_count"])+"\n")
try:
	for fname in valid_first_names:
		print(fname)
		genderizer_api_output = genderize.get([fname])
		name_gender = genderizer_api_output[0]
		writelines.append(",".join(map(str,[name_gender["name"],name_gender["gender"],name_gender["probability"],name_gender["count"]]))+"\n")
except Exception as e:
    print(e)
    print(fname)
savefig_dir = "../input/genderize/output/"
savefig_file = "%s_output_%s.csv" %(plot_code,open_file)
	
with open(savefig_dir+savefig_file, "w") as f:
	f.writelines(writelines)