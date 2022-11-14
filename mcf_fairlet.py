import numpy as np
import random
import time
from math import gcd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product

from utils import dist
# dataset
data = []
# blue/red types
blue_idx = []
blue_size = 0
red_idx = []
red_size = 0
# balance coefficient
t = 2
# pairwise distance between points
pair_dist = {}
dist_threshold = 0
# graph
G = nx.DiGraph()

def init(d, blues, reds, balance_coff, threshold):
    global blue_idx, red_idx, blue_size, red_size, data, dist_threshold, t, G
    data = d
    blue_idx = blues
    blue_size = len(blue_idx)
    red_idx = reds
    red_size = len(red_idx)
    dist_threshold = threshold
    t = balance_coff
    G = nx.DiGraph()


def gen_dist():
    global pair_dist, blue_idx, red_idx
    for bidx, i  in enumerate(blue_idx):
        for ridx, j in enumerate(red_idx):
            pair_dist[(bidx, ridx)] = dist(data[i], data[j])
def gen_graph():
    global G, blue_idx, red_idx, blue_size, red_size, data, dist_threshold, pair_dist, t
    # node properties
    # pos: where to plot on MCF graph
    # demand, capacity, cost: MCF prop
    # rk: demand < 0: supply

    # adding default node
    G.add_node('b', demand=-red_size)
    G.add_node('r', demand=blue_size)
    G.add_edge('b', 'r', cost=0, capacity=min(blue_size, red_size))
    # adding blue node
    for bidx in range(blue_size):
        G.add_node(f'B{bidx}', demand=-1)
        G.add_edge('b', f'B{bidx}', cost=0, capacity=t-1)
    # adding red node
    for ridx in range(red_size):
        G.add_node(f'R{ridx}', demand=1)
        G.add_edge(f'R{ridx}', 'r', cost=0, capacity=t-1)
    # adding additional node representing possibility
    for bidx in range(blue_size):
        for bsup in range(t):
            G.add_node(f'B{bidx}^{bsup}', demand=0)
            G.add_edge(f'B{bidx}', f'B{bidx}^{bsup}', cost=0, capacity=1)
    for ridx in range(red_size):
        for rsup in range(t):
            G.add_node(f'R{ridx}^{rsup}', demand=0)
            G.add_edge(f'R{ridx}^{rsup}', f'R{ridx}', cost=0, capacity=1)

    for (bidx, bsup, ridx, rsup) in product(range(blue_size), range(t), range(red_size), range(t)):
        dist = pair_dist[(bidx, ridx)]
        bname = f'B{bidx}^{bsup}'
        rname = f'R{ridx}^{rsup}'
        if dist <= dist_threshold:
            G.add_edge(bname, rname, cost=1, capacity=1)
        else:
            G.add_edge(bname, rname, cost=10000000, capacity=1)

def gen_fairlet():
    global G, blue_idx, red_idx, blue_size, red_size, data, dist_threshold, pair_dist, t
    _, flow = nx.network_simplex(G, weight='cost')
    fairlets = {}
    for skey in flow.keys():
        if 'B' in skey and '^' in skey and sum(flow[skey].values()) == 1:
            for ekey in flow[skey].keys():
                if flow[skey][ekey] == 1:
                    ename = ekey.split('^')[0]
                    sname = skey.split('^')[0]
                    if ename not in fairlets:
                        fairlets[ename] = [sname]
                    else:
                        fairlets[ename].append(sname)
    fairlets = [(r, b) for r, b in fairlets.items()]
    return fairlets

def gen_misc(fairlets):
    final_fairlets = []
    for f in fairlets:
        r = f[0]
        elem = [red_idx[int(r[1:])]]
        bs = f[1]
        for b in bs:
            elem.append(blue_idx[int(b[1:])])
        final_fairlets.append(elem)
    fairlets = final_fairlets
    fairlet_centers = []
    fairlet_costs = []
    for f in fairlets:
        cost_list = [(i, max([dist(data[i], data[j]) for j in f])) for i in f]
        min_cost = min(cost_list, key=lambda x:x[1])
        center, cost = min_cost[0], min_cost[1]
        fairlet_centers.append(center)
        fairlet_costs.append(cost)
    return fairlets, fairlet_centers, fairlet_costs
