import matplotlib.pyplot as plt
import networkx as nx

def deg(G):

    md = max([G.degree(u) for u in G.nodes()])

    Y = [0.0 for i in range(md + 1)]
    X = [i for i in range(md + 1)]

    for u in G.nodes():
        Y[G.degree(u)] += 1


    plt.plot(X,Y)
    plt.show()

def plot_deg_dist(G, filename):
    md = max([G.degree(u) for u in G.nodes()])

    Y = [0.0 for i in range(md + 1)]
    X = [i for i in range(md + 1)]

    for u in G.nodes():
        Y[G.degree(u)] += 1

    plt.figure()
    #plt.title("Nodes: " + str(len(G.nodes())) + " Edges: " + str(len(G.edges())) + " Fidelity: " + str(fidelity))
    #nx.draw(G, with_labels=True)
    # plt.xlabel('Degree')
    # plt.ylabel('Number of nodes')
    plt.plot(X, Y)
    plt.savefig("Plots/Metrofi/" + filename + ".png")
    plt.close()

# inputDRN = nx.read_gml('inputDRN.gml')
# plot_deg_dist(inputDRN, "inputDRN")
#
# bioDRN = nx.read_gml('GBD300.gml')
# plot_deg_dist(bioDRN, "bioDRN")
#
# refG = nx.read_gml('refG300.gml')
# plot_deg_dist(refG, "refG")
#
# origG = nx.read_gml('this_grn.gml')
# plot_deg_dist(origG, "origGRN")

#MetroFi
metroFi = nx.read_gml('metrofi.gml')
plot_deg_dist(metroFi, "metroFi")

bioMetroFi = nx.read_gml('GBD_metrofi.gml')
plot_deg_dist(bioMetroFi, "bioMetroFi")

refG_metroFi = nx.read_gml('refG_metrofi.gml')
plot_deg_dist(refG_metroFi, "refG_metroFi")

origG = nx.read_gml('this_grn.gml')
plot_deg_dist(origG, "origGRN")