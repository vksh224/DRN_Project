import networkx as nx
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt

def failed_gen(r):

    f = [[]]
    for l in r[1:]:
        current = [int(u) for u in l.split()[1:]]
        f.append(current)

    return f

def rename_graph(O):

    m = {}
    for u in O.nodes():
        m[u] = int(u)

    O = nx.relabel_nodes(O,m)
    return O

def pathcount(G,CC,S):

    #print (len(G),len(G.edges()))
    #print G.nodes()

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


    #return len(nx.triangles(G))
    return m

#modes: 0: efficiency, 1:pathcount, 2: motif
mode = 0

how_many_instances = 1

path_source_files = '/Users/satyakiroy/PycharmProjects/DRN_Project/Bhaktapur_0'
os.chdir(path_source_files)

O_List = []
B_List = []
R_List = []
K2_List = []
K4_List = []
s_List = []

for i in range(how_many_instances):

    os.chdir(str(i) + '/Data/')

    # Read files
    CC = pickle.load(open('CC_locs.p','r'))
    PoI = pickle.load(open('PoI_locs.p','r'))
    Vol = pickle.load(open('Vol_locs.p','r'))
    S = pickle.load(open('S_locs.p','r'))

    # Find source destination nodes
    CC_IDs = range(len(CC))
    PoI_IDs = range(len(CC), len(CC) + len(PoI))
    Vol_IDs = range(len(CC) + len(PoI), len(CC) + len(PoI) + len(Vol))
    S_IDs = range(len(CC) + len(PoI) + len(Vol),len(CC) + len(PoI) + len(Vol) + len(S))

    #Failed nodelist
    F = open('Failed_nodelist.txt')
    r = F.readlines()
    f = failed_gen(r)

    #Read topologies
    O = nx.read_gml('Original.gml')
    O = rename_graph(O)

    B = nx.read_gml('Bio.gml')
    B = rename_graph(B)

    R = nx.read_gml('Random.gml')
    R = rename_graph(R)

    K2 = nx.read_gml('K2.gml')
    K2 = rename_graph(K2)

    K4 = nx.read_gml('K4.gml')
    K4 = rename_graph(K4)

    s = nx.read_gml('Spanning.gml')
    s = rename_graph(s)

    #print (O.nodes())
    #print PoI_IDs

    for j in range(1,len(f)):

        print (list(set(f[j]) - set(f[j - 1])))

        O.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))
        B.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))
        R.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))
        K2.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))
        K4.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))
        s.remove_nodes_from(list(set(f[j]) - set(f[j - 1])))

        #print motif(O)
        #print motif(B)
        #print motif(K2)
        #print motif(K4)
        #print motif(s)

        if mode == 0:
            O_List.append(efficiency(O, CC_IDs, S_IDs))
            B_List.append(efficiency(B, CC_IDs, S_IDs))
            R_List.append(efficiency(R, CC_IDs, S_IDs))
            K2_List.append(efficiency(K2, CC_IDs, S_IDs))
            K4_List.append(efficiency(K4, CC_IDs, S_IDs))
            s_List.append(efficiency(s, CC_IDs, S_IDs))

        elif mode == 1:
            O_List.append(pathcount(O,CC_IDs,S_IDs))
            B_List.append(pathcount(B,CC_IDs,S_IDs))
            R_List.append(pathcount(R,CC_IDs,S_IDs))
            K2_List.append(pathcount(K2,CC_IDs,S_IDs))
            K4_List.append(pathcount(K4,CC_IDs,S_IDs))
            s_List.append(pathcount(s,CC_IDs,S_IDs))
        else:
            O_List.append(motif(O))
            B_List.append(motif(B))
            R_List.append(motif(R))
            K2_List.append(motif(K2))
            K4_List.append(motif(K4))
            s_List.append(motif(s))


        #input('')

    os.chdir(path_source_files)

timeslot_duration = 1800.0
L = [O_List,B_List,R_List,K2_List,K4_List,s_List]
print L

#Visualization
colorlist = ['r','g','b','black','magenta','purple']

for i in range(len(L)):
    plt.plot([j for j in range(len(L[i]))],L[i],marker = 'o',color = colorlist[i])

plt.xticks([j for j in range(len(L[i]))],[j * timeslot_duration for j in range(len(L[i]))])
plt.show()
