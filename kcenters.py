import numpy as np
import random
from utils import dist

data = []
center_list = []

def kcenter(d, k=5):
	global data, center_list
	data = d
	center_list = [random.randint(0, len(data)-1)]
	while len(center_list) <= k:
		remain = list(set(range(0, len(data))).difference(set(center_list)))
		new_center = max([(idx, min([dist(data[idx], data[cidx]) for cidx in center_list])) for idx in remain], key=lambda x: x[1])
		if len(center_list) < k:
			center_list.append(new_center[0])
		else:
			return center_list, new_center[1] # cost = max dist

def p2c():
	global data, center_list
	return [(idx, min([(cidx, dist(data[idx], data[cidx])) for cidx in center_list], key=lambda x: x[1])[0]) for idx in range(len(data))]
