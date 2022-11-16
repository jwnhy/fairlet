import pandas as pd
import numpy as np

dataname = "census"
fair_key = "marital"
fair_val = ["single", "married"]
dist_key = ["age", "balance", "duration"]
seed = 21
sample_size = [650, 350]
dist_threshold = 400
normalization = False
data = None

def load(json_config):
	global dataname, fair_key, fair_val, dist_key, seed, sample_size, normalization, data, dist_threshold
	fair_key = json_config[dataname]['fair_key']
	fair_val = json_config[dataname]['fair_val']
	dist_key = json_config[dataname]['dist_key']
	dist_threshold = json_config[dataname]['dist_threshold']
	if dataname == 'bank':
		data = pd.read_csv('data/bank-full.csv', sep=';')
	elif dataname == 'census':
		data = pd.read_csv('data/uci_census.csv')
	# remove out-of-range data points
	data = data[data[fair_key].isin(fair_val)]
	# collect statistics of fair attributes
	fair_idx = data[fair_key].value_counts().index
	fair_cnt = data[fair_key].value_counts().values
	fair_stat = dict(zip(fair_idx, fair_cnt)).items()
	fair_stat = sorted(fair_stat, key=lambda x:x[1], reverse=True)
	# only keep relevant attributes
	data = data[[fair_key] + dist_key].copy()
	# encodes data to 1/0
	data[fair_key] = np.where(data[fair_key] == fair_stat[0][0], 1, 0)
	print(f"Encoding {fair_stat[0][0]} as 1, and {fair_stat[1][0]} as 0\n")
	# normalize the distance if needed
	if normalization:
		print("Normalization: True")
		for col in data.columns:
			col_min, col_max = np.min(data[col]), np.max(data[col])
			data[col] = (data[col] - col_min) / (col_max - col_min)

def sample():
	global dataname, fair_key, fair_val, dist_key, seed, sample_size, normalization, data
	major_size, minor_size = max(sample_size), min(sample_size)
	majority = data[data[fair_key]==1].sample(major_size, random_state=seed)
	minority = data[data[fair_key]==0].sample(minor_size, random_state=seed)
	df = pd.concat([majority, minority], ignore_index=True)
	df = df.sample(frac=1, random_state=seed)
	data = df.reset_index(drop=True)
	blues = list(data[data[fair_key]==1].index)
	reds = list(data[data[fair_key]==0].index)
	data_list = [list(i) for i in np.array(data)]
	return blues, reds, data_list, dist_threshold