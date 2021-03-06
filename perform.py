import networkx as nx
import pickle
import os
import numpy as np

#Motif files
def generate_motif_files(number_of_nodes, all_topologies_list, failure_perc):
    with open("GraphExperiments/motif_" + str(number_of_nodes) + ".txt", "a") as f:
        line_str = str(round(failure_perc, 2)) + " "
        for eachG in all_topologies_list:
            line_str += str(motif(eachG)) + " "
        f.write(line_str +"\n")

#NE files
def generate_NE_files(number_of_nodes, all_topologies_list, failure_perc, CC, S):
    with open("GraphExperiments/NE_" + str(number_of_nodes) + ".txt", "a") as f:
        line_str = str(round(failure_perc, 2)) + " "
        for eachG in all_topologies_list:
            eff = efficiency(eachG, CC, S)
            line_str += str(round(eff, 3)) + " "
        f.write(line_str + "\n")

#Path Count files
def generate_NE_files(number_of_nodes, all_topologies_list, failure_perc, CC, S):
    with open("GraphExperiments/Path_" + str(number_of_nodes) + ".txt", "a") as f:
        line_str = str(round(failure_perc, 2)) + " "
        for eachG in all_topologies_list:
            eff = efficiency(eachG, CC, S)
            line_str += str(round(eff, 3)) + " "
        f.write(line_str + "\n")

def failures(G,f):
    n = int(f * 0.05 * len(G))
    i = 0
    while(i <= n):
        i = i + 1
        G.remove_node(np.random.choice(G.nodes()))
    return G

def pathcount(G,CC,S):
    p = 0.0
    for s in S:
        if s not in G.nodes():
            continue
        for c in CC:
            if c not in G.nodes():
                continue

            if nx.has_path(G,s,c):
                paths = nx.all_simple_paths(G, source = s, target = c,cutoff = 4)
                p += len(list(paths))
    return p

def efficiency(G,CC,S):
    e = 0.0
    den = 0.0
    for s in S:
        if s not in G.nodes():
            continue

        for c in CC:
            if c not in G.nodes():
                continue

            if nx.has_path(G, s, c):
                l = nx.shortest_path_length(G, source = s, target = c)
                e = e + 1.0/float(l)

            den = den + 1.0

    if den == 0:
        return 0

    return float(e)/den

def motif(G):
    m = 0
    for u in G.nodes():
        for v in G.nodes():
            if v <= u:
                continue

            for w in G.nodes():
                if w <= v:
                    continue

                if G.has_edge(u, v) and G.has_edge(v, w) and G.has_edge(u, w):
                    m += 1
    return m

def perf(G,CC,S):
    m = motif(G)
    print ("Number of nodes:",len(G))
    print ("Number of motifs in G:",m)
    #print("Number of isolated nodes in G:", len(nx.isolates(G)))
    print ("Motifs density in G:",float(m)/float(len(G)))

    e = efficiency(G,CC,S)
    print("Average network efficiency of G:", e)

    p = pathcount(G,CC,S)
    print("Path count of G:", p)

curr = os.getcwd()

MC_G1 = pickle.load(open("GRN_Centrality.p", "rb"))
motifG = sum([each for each in MC_G1.values()])
motifG /= 3

print("Motifs density in GRN:", float(motifG) / 4441.0)

os.chdir('kathmandu')
CC = pickle.load(open("HO.p", "rb"))
S = pickle.load(open("NO.p", "rb"))

refG = nx.read_gml('refG.gml')
GBD = nx.read_gml('GBD.gml')
SP = nx.read_gml('S.gml')
R = nx.read_gml('R.gml')
K2 = nx.read_gml('KR2.gml')
K4 = nx.read_gml('KR4.gml')
K8 = nx.read_gml('KR8.gml')

number_of_nodes = len(GBD.nodes())

for ii in range(4,5):
    ss = (ii + 2) * 50
    print ("Number of nodes:", ss)
    print ("--------------------\n")

    for f in range(5):

        print("Failure percentage:", round(f * 0.05, 2))

        refG = failures(refG,f)
        GBD = failures(GBD, f)
        SP = failures(SP, f)
        R = failures(R, f)
        K2 = failures(K2, f)
        K4 = failures(K4, f)
        K8 = failures(K8, f)

        os.chdir(curr)

        print('refG.gml')
        perf(refG.to_undirected(), CC, S)

        print('GBD.gml')
        perf(GBD.to_undirected(), CC, S)

        print('S.gml')
        perf(SP.to_undirected(), CC, S)

        print('R.gml')
        perf(R.to_undirected(), CC, S)

        print('KR2.gml')
        perf(K2, CC, S)

        print('KR4.gml')
        perf(K4, CC, S)

        print('KR8.gml')
        perf(K8, CC, S)

        all_topologies_list = [refG.to_undirected(), GBD.to_undirected(), SP.to_undirected(), R.to_undirected(), K2, K4, K8]
        generate_motif_files(number_of_nodes, all_topologies_list, f * 0.05)
        generate_NE_files(number_of_nodes, all_topologies_list, f * 0.05, CC, S)

        print("\n")



