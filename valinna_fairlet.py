from utils import dist

# dataset
data = []
# blue/red types
blue_idx = []
blue_size = 0
red_idx = []
red_size = 0

# balanced parameters
balance_p1 = 0
balance_p2 = 0

def pre_processing():
    global blue_idx, red_idx, blue_size, red_size
    if blue_size - red_size > 0:
        temp = red_idx
        red_idx = blue_idx
        blue_idx = temp
    red_size = len(red_idx)
    blue_size = len(blue_idx)    
        
def init_valinna(d, p, q, blues, reds):
    global blue_idx, red_idx, blue_size, red_size, data, balance_p1, balance_p2
    blue_idx = blues
    blue_size = len(blue_idx)
    red_idx = reds
    red_size = len(red_idx)
    balance_p1 = p
    balance_p2 = q
    data = d
    pre_processing()
    assert(blue_size + red_size > 0)
    
    
def gen_fairlet_valinna(point_indexs, fairlets, fairlet_centers, costs):
    fairlet_costs = []
    center  = 0
    min_max_distance = None
    for i in point_indexs:
        max_distance = 0
        for j in point_indexs:
            max_distance = max(max_distance, dist(data[i],data[j]))
        fairlet_costs.append((i,max_distance))
        if min_max_distance is None or min_max_distance > max_distance:
            min_max_distance = max_distance
            center = i
    fairlets.append(point_indexs)
    fairlet_centers.append(center)
    costs.append(min_max_distance)
            
            
def decompose():
    fairlets = []
    fairlet_centers = []
    fairlet_costs = []
    current_blue_num = 0
    current_red_num = 0

    while ((red_size - current_red_num) - (blue_size - current_blue_num)) >= (balance_p2 - balance_p1) and (red_size - current_red_num) >= balance_p2 and (blue_size - current_blue_num) >= balance_p1:
        gen_fairlet_valinna(red_idx[current_red_num: (current_red_num + balance_p2)] + 
                            blue_idx[current_blue_num: (current_blue_num + balance_p1)], fairlets, fairlet_centers, fairlet_costs)
        current_red_num += balance_p2
        current_blue_num += balance_p1
        
    
          
    if ((red_size - current_red_num) != (blue_size - current_blue_num)) and ((blue_size - current_blue_num) >= balance_p1):
        gen_fairlet_valinna(red_idx[current_red_num: current_red_num + (red_size - current_red_num) - (blue_size - current_blue_num) + balance_p1]
                            + blue_idx[current_blue_num: (current_blue_num + balance_p1)], fairlets, fairlet_centers, fairlet_costs)
        current_red_num += (red_size - current_red_num) - (blue_size - current_blue_num) + balance_p1
        current_blue_num += balance_p1
    elif ((red_size - current_red_num) + (blue_size - current_blue_num)) >= 1 and ((red_size - current_red_num) + (blue_size - current_blue_num)) <= (balance_p1 + balance_p2):
        gen_fairlet_valinna(red_idx[current_red_num:] + blue_idx[current_blue_num:], fairlets, fairlet_centers, fairlet_costs)
        current_red_num = red_size
        current_blue_num = blue_size    
    
    offset = red_size - current_red_num
    for i in range(offset):
        # print(i,red_size,blue_size,len(red_idx),len(blue_idx))    
        gen_fairlet_valinna([red_idx[current_red_num + i], blue_idx[current_blue_num + i]], 
                            fairlets, fairlet_centers, fairlet_costs)

    return fairlets, fairlet_centers, fairlet_costs
