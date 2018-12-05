from construct_NepalDRN_utility import *
from Centrality import motif
from writeFile import *

#This function returns the actual indirect links. For example, if responder 29 visits CC 0, PoI 1 and 2, then
# following links exist: 0 - 29, 1 - 29, 2 - 29
def get_indirect_tier1_tier2_links(G, Res_visiting_IDs_list):
    count = 0 #Count number of responders
    for res in Res_visiting_IDs_list:
        for u in res:
            if G.has_edge(u, num_of_nodes + count) == False:
                G.add_edge(u, num_of_nodes + count)
                # print("Edge: ", r, num_of_nodes + count)

            if G.has_edge(num_of_nodes + count, u) == False:
                G.add_edge(num_of_nodes + count, u)
        count = count + 1

#This function returns the actual indirect links. For example, if responder 29 visits CC 0, PoI 1 and 2, then
# following links exist: 0 - 29, 1 - 29, 2 - 29
def get_tier1_tier2_indirect_links(G, node_visited_by_all_responders_dict):
    # could be node_id, res_list
    for node_id, res_list in node_visited_by_all_responders_dict.items():
        for res_id in res_list:
            if G.has_edge(node_id, res_id) == False:
                G.add_edge(node_id, res_id)

            if G.has_edge(res_id, node_id) == False:
                G.add_edge(res_id, node_id)

#Get links between tier 1 and tier 2 nodes
# This function returns the representational links. For example, if responder 29 visits CC 0, PoI 1 and 2, then
# following links exist: 0 - 1, 1 - 2, 0 - 2
def get_tier1_tier2_links(G, res_visiting_all_nodes_dict):
    for res_id, node_list in res_visiting_all_nodes_dict.items():
        for u in node_list:
            for v in node_list:
                if u != v and G.has_edge(u, v) == False:
                    G.add_edge(u, v)
                if u != v and G.has_edge(v, u) == False:
                    G.add_edge(v, u)


def create_static_network(res_visiting_all_nodes_dict, node_visited_by_all_responders_dict, start_time, end_time):
    G = nx.DiGraph()
    # For ONE simulator
    real_world_G = nx.DiGraph()

    #Add DRN nodes
    for id in CC_IDs:
        G.add_node(id)
        real_world_G.add_node(id)

    for id in PoI_IDs:
        G.add_node(id)
        real_world_G.add_node(id)

    for id in Vol_IDs:
        G.add_node(id)
        real_world_G.add_node(id)

    for id in S_IDs:
        G.add_node(id)
        real_world_G.add_node(id)

    #add responders as nodes in real world network. Note they are not part of nodes in the Original DRN
    for id in Res_IDs:
        real_world_G.add_node(id)

    #Add edges
    get_tier1_tier2_indirect_links(real_world_G, node_visited_by_all_responders_dict)
    print("all_nodes_visited_by_a_res_dict", node_visited_by_all_responders_dict.items()[1])

    get_tier1_tier2_links(G, res_visiting_all_nodes_dict)
    print("Res_visiting_IDs_dict", res_visiting_all_nodes_dict.items()[1])

    sparseG = G.copy()

    V = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)
    #Add edges between each pair of nodes for the given time interval
    with open(loc_des_folder + "ext_position_" + str(V) + ".txt", "r") as f:
        node_pos_lines = f.readlines()[1:]

    for line1 in node_pos_lines:
        line1_arr = line1.strip().split(" ")
        line1_arr = [int(ele) for ele in line1_arr]

        for line2 in node_pos_lines:
            line2_arr = line2.strip().split(" ")
            line2_arr = [int(ele) for ele in line2_arr]

            # u != v, and start_time < t(u), t(v) <= end_time, and t(u) == t(v) and dist(u, v) < range
            if line1_arr[1] != line2_arr[1] \
                and line1_arr[0] >= start_time and line1_arr[0] <= end_time \
                and line2_arr[0] >= start_time and line2_arr[0] <= end_time \
                and line1_arr[0] == line2_arr[0] \
                and euclideanDistance(line1_arr[2], line1_arr[3], line2_arr[2], line2_arr[3]) <= bt_range:

                G.add_edge(line1_arr[1], line2_arr[1])
                real_world_G.add_edge(line1_arr[1], line2_arr[1])

                if S_IDs.__contains__(line1_arr[1]) and S_IDs.__contains__(line2_arr[1]):
                    continue
                else:
                    sparseG.add_edge(line1_arr[1], line2_arr[1])

    print("G: # Nodes", len(G), len(sparseG))
    print("G: # Edges", len(G.edges()), len(sparseG.edges()))
    print("G: Density:", float(len(G.edges()) * 2) / (len(G) * (len(G) - 1)))

    print("Real world G: # Nodes", len(real_world_G))
    print("Real world G: # Edges", len(real_world_G.edges()))
    print("Real world G: Density:", float(len(real_world_G.edges()) * 2) / (len(real_world_G) * (len(real_world_G) - 1)))

    return G, sparseG, real_world_G


#Main Starts here

#Get CC, PoI, Vol, S, Res (in this order for node ID)
CC_locs = pickle.load(open(data_directory + "CC_locs.p", "rb"))
PoI_locs = pickle.load(open(data_directory + "PoI_locs.p", "rb"))
Vol_locs = pickle.load(open(data_directory + "Vol_locs.p", "rb"))
S_locs = pickle.load(open(data_directory + "S_locs.p", "rb"))
Res_paths = pickle.load(open(data_directory + "Res_paths.p", "rb"))
res_visiting_all_nodes_dict = pickle.load(open(data_directory + "res_visiting_all_nodes.p", "rb"))
node_visited_by_all_responders_dict = pickle.load(open(data_directory + "node_visited_by_all_responders.p", "rb"))

#Node that responders do not belong to node list (in the Orig DRN)
num_of_nodes = len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs)

#Except survivors
CC_IDs = [i for i in range(len(CC_locs))]
PoI_IDs = [i for i in range(len(CC_locs), len(CC_locs) + len(PoI_locs))]
Vol_IDs = [i for i in range(len(CC_locs) + len(PoI_locs), len(CC_locs) + len(PoI_locs) + len(Vol_locs))]
S_IDs = [i for i in range(len(CC_locs) + len(PoI_locs) + len(Vol_locs), len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs))]

#only for real world network (i.e., ONE simulator)
Res_IDs = [i for i in range(len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs), len(CC_locs) + len(PoI_locs) + len(Vol_locs) + len(S_locs) + len(Res_paths))]

print ("CC-count ", len(CC_locs), "s-id", CC_IDs[0], "e-id", CC_IDs[len(CC_IDs) - 1])
print ("PoI-count ", len(PoI_locs), "s-id", PoI_IDs[0], "e-id", PoI_IDs[len(PoI_IDs) - 1])
print ("Vol-count ", len(Vol_locs), "s-id", Vol_IDs[0], "e-id", Vol_IDs[len(Vol_IDs) - 1])
print ("S-count ", len(S_locs), "s-id", S_IDs[0], "e-id", S_IDs[len(S_IDs) - 1])
print ("Res-count ", len(Res_paths), "s-id", Res_IDs[0], "e-id", Res_IDs[len(Res_IDs) - 1])

#print("last node_id", S_IDs[len(S_IDs) - 1])
#Res_visiting_IDs_list = responder_visiting_IDs()

#Need to create these graphs for each time interval e.g., [0, 900; 900, 1800; 1800, 2700; 2700, 3600]
start_time = 0
end_time = 1800

G, sparseG, real_world_G = create_static_network(res_visiting_all_nodes_dict, node_visited_by_all_responders_dict, start_time, end_time)


nei_o = writeF(real_world_G, 0)
orig_neighList_filename = 'O_N' + str(len(real_world_G.nodes())) + ".txt"
print("Orig - Neighbor list filename", orig_neighList_filename)
f = open(neigh_des_folder + orig_neighList_filename,'w')
f.write(nei_o)
f.close()

#Non-increasing motif central nodes
# MC_G = motif(sparseG)
# MC_G = [each[0] for each in sorted(MC_G.items(), key=lambda x: x[1], reverse=True)]
# allNodes = MC_G

#Non-increasing degree central nodes
# degrees = G.degree()
# allNodes = [each[0] for each in sorted(degrees.items(), key=lambda x: x[1], reverse=True)]

# t1 = allNodes[:int(t1_ratio * len(G))]
# t2 = allNodes[int(t1_ratio * len(G)):int(t1_ratio * len(G)) + int(t2_ratio * len(G))]
# t3 = [u for u in G.nodes() if u not in t1 and u not in t2]

t1 = CC_IDs
t2 = []
for id in PoI_IDs:
    t2.append(id)
for id in Vol_IDs:
    t2.append(id)
t3 = S_IDs
pickle.dump(t1, open(data_directory + 'HO.p','wb'))
pickle.dump(t2, open(data_directory + 'SO.p','wb'))
pickle.dump(t3, open(data_directory + 'NO.p','wb'))

nx.write_gml(G, directory + "Orig_NepalDRN.gml")
nx.write_gml(sparseG, directory + "Sparse_Orig_NepalDRN.gml")

plot_graph(G, plot_directory + "Orig_NepalDRN")
plot_graph(sparseG, plot_directory + "Sparse_Orig_NepalDRN")

