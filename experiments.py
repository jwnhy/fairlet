import time
import kcenters
from utils import dist, balance

def run_experiments(degrees, data, fairlets, fairlet_centers, verbose=True):
	curr_degrees = []
	curr_costs = []
	curr_balances = []

	for degree in range(1, min(degrees+1, len(fairlet_centers)), 1):
		start_time = time.time()
		
		centers, cost = kcenters.kcenter([data[i] for i in fairlet_centers], k=degree)
		mapping = kcenters.p2c()
		
		final_clusters = []
		for fairlet_id, final_cluster in mapping:
			for point in fairlets[fairlet_id]:
				final_clusters.append((point, fairlet_centers[final_cluster]))
				
		centers = [fairlet_centers[i] for i in centers]
		curr_degrees.append(degree)
		curr_costs.append(max([min([dist(data[j], i) for j in centers]) for i in data]))
		curr_balances.append(balance(data, centers, final_clusters))
		
		if verbose:
			print("Time for # Cluster %d - %.3f seconds."%(degree, time.time() - start_time))

	return curr_degrees, curr_costs, curr_balances