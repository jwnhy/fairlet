import numpy as np
import matplotlib.pyplot as plt

def dist(a, b):
	return np.linalg.norm(x=np.array(a)-np.array(b), ord=2)

def balance(data, centers, mapping):
	p_dict = dict([(i, 0) for i in centers])
	q_dict = dict([(i, 0) for i in centers])
	for (d, c) in mapping:
		if data[d][0] == 1:
			p_dict[c] += 1
		else:
			q_dict[c] += 1
	final_balance = 100000000
	for c in centers:
		p = p_dict[c]
		q = q_dict[c]
		if p == 0 or q == 0:
			balance = 0
		else:
			balance = min(float(p/q), float(q/p))
		final_balance = min(balance, final_balance)

	return final_balance

def plot_analysis(degrees, costs, balances, step_size):
	fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 4))
	ax[0].plot(costs, marker='o', markersize=10, color='blue')
	ax[0].set_xticks(list(range(0, len(degrees), step_size))) 
	ax[0].set_xticklabels(list(range(min(degrees), max(degrees)+1, step_size)), fontsize=14)
	ax[1].plot(balances, marker='o',markersize=10,color='red')
	ax[1].set_xticks(list(range(0, len(degrees), step_size))) 
	ax[1].set_xticklabels(list(range(min(degrees), max(degrees)+1, step_size)), fontsize=14)
	plt.show()